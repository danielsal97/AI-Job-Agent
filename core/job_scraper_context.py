from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class JobScraperContext:
    def __init__(self, scraper):
        self.scraper = scraper

    def scrape_jobs(self, base_url, use_requests=False):
        """
        Scrape jobs from the provided URL using Selenium, BeautifulSoup, and Requests.
        """
        # consider to delete this part not i use
        if use_requests:
            print("Using Requests for scraping...")
            html = self.scraper.fetch_with_requests(base_url)
            if html:
                return self.scraper.parse_with_beautifulsoup(html)
            else:
                return []

        # Use Selenium for JavaScript-heavy pages
        print("Using Selenium for scraping...")
        driver = webdriver.Safari()  # Use your preferred browser
        wait = WebDriverWait(driver, 10)
        driver.get(base_url)

        all_jobs = self.scraper.scrape_with_selenium(driver, wait)

        driver.quit()
        return all_jobs