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


class HybridJobScraper:
    def __init__(self, selectors, base_url):
        """
        Initialize the scraper with website-specific selectors and base URL.
        """
        self.selectors = selectors
        self.base_url = base_url

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
            job_details = self.extract_job_details(driver, wait, job["link"])
            detailed_jobs.append(job_details)

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