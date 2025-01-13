import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class LinkedInJobScraper:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = self.init_browser()

    def init_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def authenticate(self):
        self.driver.get("https://www.linkedin.com/login")
        email_input = self.driver.find_element(By.ID, "username")
        password_input = self.driver.find_element(By.ID, "password")
        email_input.send_keys(self.email)
        password_input.send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "global-nav-search"))
        )
        print("Logged in to LinkedIn")

    def search_jobs(self, search_string):
        self.driver.get(f"https://www.linkedin.com/jobs/search/?keywords={search_string}")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results__list"))
        )
        jobs = self.driver.find_elements(By.CLASS_NAME, "job-card-container")
        job_data = []
        for job in jobs:
            title = job.find_element(By.CLASS_NAME, "job-card-list__title").text
            company = job.find_element(By.CLASS_NAME, "job-card-container__company-name").text
            location = job.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text
            link = job.find_element(By.CLASS_NAME, "job-card-list__title").get_attribute("href")
            job_data.append({"title": title, "company": company, "location": location, "link": link})
        return job_data

    def store_jobs(self, job_data, file_path="jobs.csv"):
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["title", "company", "location", "link"])
            writer.writeheader()
            for job in job_data:
                writer.writerow(job)
        print(f"Jobs stored in {file_path}")

    def close(self):
        self.driver.quit()

# Example usage:
# scraper = LinkedInJobScraper(email="your_email", password="your_password")
# scraper.authenticate()
# jobs = scraper.search_jobs("Software Engineer")
# scraper.store_jobs(jobs)
# scraper.close()
