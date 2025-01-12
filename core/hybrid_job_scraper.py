import hashlib
import psycopg2
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException,
)
from bs4 import BeautifulSoup
import time
import requests

DATABASE = {
    'dbname': 'jobs_db',
    'user': 'danielsa',
    'password': '',  # Add your PostgreSQL password if needed
    'host': 'localhost',
    'port': 5432
}

class HybridJobScraper:
    def __init__(self, selectors, base_url, db_config=DATABASE):
        """
        Initialize the scraper with website-specific selectors, base URL, and database config.
        """
        self.selectors = selectors
        self.base_url = base_url
        self.db_config = db_config  # Pass database connection info

    def generate_uuid(self, job_id, job_title, company, link):
        """
        Generate a unique UUID based on job_id, job_title, company, and link.
        """
        unique_string = f"{job_id}_{job_title}_{company}_{link}"
        return hashlib.md5(unique_string.encode()).hexdigest()

    def check_job_exists(self, job_link):
        """
        Check if the job with the given job_link exists in the database.
        Return `True` if the job exists, otherwise return `False`.
        """
        query = "SELECT 1 FROM jobs WHERE link = %s;"
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute(query, (job_link,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result is not None  # Job exists if result is not None
        except Exception as e:
            print(f"Database error while checking job existence: {e}")
            return False

    def insert_job_to_db(self, job_id, company, title, description, link, location):
        """Insert job into the database if it doesn't exist."""
        if self.check_job_exists(link):
            print(f"Job with link {link} already exists. Skipping.")
            return

        # Ensure job_id is unique by generating a UUID if it's missing or "Unknown"
        if not job_id or job_id.strip() == "" or job_id == "Unknown":
            job_id = self.generate_uuid(job_id, title, company, link)

        # Default company if it is None or empty
        if not company or company.strip() == "":
            company = "Unknown"

        query = """
        INSERT INTO jobs (job_id, company, title, description, link, location)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (job_id, company, link) DO NOTHING;  -- Prevent duplicate entries
        """
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute(query, (job_id, company, title, description, link, location))
            conn.commit()
            print(f"Job '{title}' added to the database successfully!")
        except Exception as e:
            print(f"Error inserting job into database: {e}")
        finally:
            cursor.close()
            conn.close()

    def fetch_with_requests(self, url):
        """
        Fetch a page using Requests (for static pages or APIs).
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Requests error: {e}")
            return None

    def parse_with_beautifulsoup(self, html):
        """
        Parse HTML content with BeautifulSoup and extract job links.
        """
        soup = BeautifulSoup(html, "html.parser")
        jobs = []
        for job_card in soup.select(self.selectors["job_card"]):
            job_title = job_card.select_one(self.selectors["job_title"])
            if job_title:
                job_link = urljoin(self.base_url, job_title.get("href"))
                jobs.append({
                    "title": job_title.text.strip(),
                    "link": job_link,
                })
        return jobs

    def extract_job_details(self, driver, wait, job_link):
        """
        Visit each job link and extract detailed information.
        """
        print(f"Extracting details for job: {job_link}")
        driver.get(job_link)
        job_details = {
            "title": "Unknown",
            "location": "Unknown",
            "date": "Unknown",
            "description": "Unknown",
            "link": job_link,
        }

        try:
            job_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.selectors["job_title_detail"])))
            job_details["title"] = job_title.text.strip()
        except Exception as e:
            print(f"Error extracting job title: {e}")

        try:
            job_location = driver.find_element(By.CSS_SELECTOR, self.selectors["job_location"])
            job_details["location"] = job_location.text.strip()
        except Exception as e:
            print(f"Error extracting job location: {e}")

        try:
            job_date = driver.find_element(By.CSS_SELECTOR, self.selectors["job_date"])
            job_details["date"] = job_date.text.strip()
        except Exception as e:
            print(f"Error extracting job date: {e}")

        try:
            job_description = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.selectors["job_description"]))
            )
            job_details["description"] = job_description.text.strip()
        except Exception as e:
            print(f"Error extracting job description: {e}")

        return job_details

    def scrape_with_selenium(self, driver, wait):
        """
        Scrape jobs using Selenium for JavaScript-heavy pages.
        """
        jobs = []
        detailed_jobs = []

        while True:
            try:
                # Wait for job cards to load
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.selectors["job_card"])))

                # Extract jobs with BeautifulSoup for better performance
                html = driver.page_source
                jobs.extend(self.parse_with_beautifulsoup(html))

                # Navigate to the next page
                next_button = self.locate_next_button(driver, wait)
                if not next_button:
                    print("No more pages to navigate. Scraping complete.")
                    break
                next_button.click()
                time.sleep(2)  # Small delay for the next page to load
            except (TimeoutException, StaleElementReferenceException) as e:
                print(f"Error during Selenium scraping: {e}")
                break

        # Visit each job link to extract detailed information
        for job in jobs:
            uuid = self.generate_uuid(job.get("id", ""), job["title"], self.base_url, job["link"])

            # Check if the job already exists in the database
            if self.check_job_exists(job["link"]):
                print(f"Skipping job: {job['title']}. Already exists in the database.")
                continue

            job_details = self.extract_job_details(driver, wait, job["link"])
            detailed_jobs.append(job_details)

            # Insert job into the database
            self.insert_job_to_db(job.get("id", ""), job.get("company", "Unknown"), job["title"], job_details["description"], job["link"], job_details["location"])

        return detailed_jobs

    def locate_next_button(self, driver, wait):
        """
        Locate the 'Next' button dynamically to avoid stale element issues.
        """
        try:
            if self.selectors["next_button_type"] == "link":
                return driver.find_element(By.CSS_SELECTOR, self.selectors["next_button"])
            elif self.selectors["next_button_type"] == "button":
                return wait.until(
                    EC.element_to_be_clickable((By.XPATH, self.selectors["next_button"]))
                )
        except (NoSuchElementException, TimeoutException):
            print("No valid 'Next' button found.")
            return None