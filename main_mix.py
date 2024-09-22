import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException, StaleElementReferenceException
from main import init_browser, LinkedInBotFacade, ConfigValidator, FileManager, Resume
from linkedIn_easy_applier import LinkedInEasyApplier
import logging
import os
from PIL import Image
from io import BytesIO
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
from gpt import GPTAnswerer
import json
import random
import pika

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# RabbitMQ configuration
RABBITMQ_HOST = 'localhost'  # Change this if your RabbitMQ server is on a different host
JOB_QUEUE = 'linkedin_jobs_to_apply'
RESULT_QUEUE = 'linkedin_application_results'

def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=JOB_QUEUE, durable=True)
    channel.queue_declare(queue=RESULT_QUEUE, durable=True)
    return connection, channel

def save_screenshot_with_error(browser, error_msg, element_name):
    """Save a screenshot with error message when a selector fails"""
    screenshot = browser.get_screenshot_as_png()
    img = Image.open(BytesIO(screenshot))
    
    # Create 'screenshots' directory if it doesn't exist
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
    
    # Save the screenshot with a unique name
    filename = f"screenshots/{element_name}_{int(time.time())}.png"
    img.save(filename)
    
    # Save error message to a text file
    error_filename = f"screenshots/{element_name}_{int(time.time())}_error.txt"
    with open(error_filename, 'w') as f:
        f.write(error_msg)
    
    # Log the error and screenshot location
    logging.error(f"{error_msg}. Screenshot saved as {filename}. Error details saved as {error_filename}")

def login_to_linkedin(bot: LinkedInBotFacade, email: str, password: str):
    logging.debug("Logging into LinkedIn")
    try:
        bot.start_login(email, password)
        logging.info("Logged into LinkedIn successfully")
    except Exception as e:
        save_screenshot_with_error(bot.driver, f"Login failed: {str(e)}", "login_error")
        raise

def perform_searches(browser, wait):
    logging.debug("Performing job searches with specified filters")
    browser.get("https://www.linkedin.com/jobs/search/?keywords=react&f_TPR=r604800&f_E=1%2C2%2C3%2C4%2C5%2C6&f_SB2=6&f_WT=2%2C3&f_AL=true")
    logging.info("Search performed with specified parameters")

def click_search_button(browser, wait):
    logging.debug("Clicking the search button")
    try:
        search_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#global-nav-search > div > div.jobs-search-box__container.jobs-search-box > button.jobs-search-box__submit-button.artdeco-button.artdeco-button--2.artdeco-button--secondary")))
        search_btn.click()
        logging.info("Search button clicked")
    except (NoSuchElementException, ElementNotInteractableException, TimeoutException) as e:
        save_screenshot_with_error(browser, f"Search button error: {str(e)}", "search_button_error")
        raise

def get_job_listings(browser, wait):
    logging.debug("Retrieving job listings")
    max_retries = 3
    for attempt in range(max_retries):
        try:
            job_list = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__list > div > ul > li")))
            jobs = []
            for job in job_list:
                job_title = job.find_element(By.CSS_SELECTOR, "h3").text
                job_id = job.get_attribute("data-job-id")
                jobs.append({'title': job_title, 'id': job_id})
                logging.debug(f"Found job: {job_title} with ID: {job_id}")
            return jobs
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException) as e:
            if attempt < max_retries - 1:
                logging.warning(f"Error retrieving job listings (attempt {attempt + 1}): {str(e)}. Retrying...")
                time.sleep(random.uniform(1, 3))
            else:
                save_screenshot_with_error(browser, f"Job listings not found: {str(e)}", "job_listings_not_found")
                return []

def navigate_pagination(browser, wait):
    logging.debug("Checking for next page in pagination")
    try:
        next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='View next page']")))
        if next_button.is_enabled():
            logging.info("Next page button found")
            return next_button
    except (NoSuchElementException, TimeoutException) as e:
        logging.info("Next page button not found or not clickable")
    return None

def apply_to_job(browser, job_id, easy_applier, applied_jobs):
    if job_id in applied_jobs:
        logging.info(f"Job ID {job_id} already applied, skipping")
        return

    logging.debug(f"Applying to job ID: {job_id}")
    try:
        job_url = f"https://www.linkedin.com/jobs/search/?currentJobId={job_id}&distance=100&f_E=1%2C3&f_JT=F%2CC%2CP%2CT%2CO&f_LF=f_AL&f_WT=2&keywords=Magento%20developer&location=United%20States"
        browser.get(job_url)
        time.sleep(random.uniform(2, 4))  # Random wait to avoid detection

        easy_applier.fill_up()
        
        if easy_applier._next_or_submit():
            logging.info(f"Application to job ID {job_id} was successful")
            applied_jobs.add(job_id)
            save_applied_job(job_id, 'linkedin-pass')
        else:
            error_msg = f"Application to job ID {job_id} may have failed"
            save_screenshot_with_error(browser, error_msg, f"job_{job_id}_application_failed")
            save_applied_job(job_id, 'linkedin-fail')
    except Exception as e:
        save_screenshot_with_error(browser, f"Error during application: {str(e)}", f"job_{job_id}_application_error")
        save_applied_job(job_id, 'linkedin-fail')

def save_applied_job(job_id, status):
    filename = f"{status}.json"
    try:
        with open(filename, 'r+') as f:
            data = json.load(f)
            data.append(job_id)
            f.seek(0)
            json.dump(data, f)
    except FileNotFoundError:
        with open(filename, 'w') as f:
            json.dump([job_id], f)

def load_applied_jobs():
    applied_jobs = set()
    for filename in ['linkedin-pass.json', 'linkedin-fail.json']:
        try:
            with open(filename, 'r') as f:
                applied_jobs.update(json.load(f))
        except FileNotFoundError:
            pass
    return applied_jobs

def main_mix():
    connection = None
    browser = None
    try:
        browser = init_browser()
        wait = WebDriverWait(browser, 10)
        
        data_folder = Path("data_folder")
        secrets_file, config_file, plain_text_resume_file, output_folder = FileManager.validate_data_folder(data_folder)
        parameters = ConfigValidator.validate_config(config_file)
        email, password, gemini_api_key = ConfigValidator.validate_secrets(secrets_file)
        parameters['uploads'] = FileManager.file_paths_to_dict(None, plain_text_resume_file)
        parameters['outputFileDirectory'] = output_folder

        gpt_answerer = GPTAnswerer(
            openai_api_key=parameters.get('openai_api_key'),
            google_api_key=gemini_api_key
        )

        # Initialize Resume with opened file instead of Path object
        with open(parameters['uploads']['plainTextResume'], 'r') as resume_file:
            resume_obj = Resume(resume_file)

        # Initialize LinkedInBotFacade with the browser
        bot = LinkedInBotFacade(browser, wait)
        bot.set_secrets(email, password)
        bot.set_resume(resume_obj)
        # Remove the following line as it's causing the error
        # bot.set_gpt_answerer(gpt_answerer)

        login_to_linkedin(bot, email, password)
        perform_searches(browser, wait)
        click_search_button(browser, wait)

        # Connect to RabbitMQ
        connection, channel = connect_to_rabbitmq()

        applied_jobs = load_applied_jobs()
        easy_applier = LinkedInEasyApplier(browser, wait, gpt_answerer)  # Pass gpt_answerer here

        while True:
            jobs = get_job_listings(browser, wait)
            for job in jobs:
                channel.basic_publish(
                    exchange='',
                    routing_key=JOB_QUEUE,
                    body=json.dumps(job),
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                    ))
                logging.info(f"Job ID {job['id']} sent to RabbitMQ queue")

            next_button = navigate_pagination(browser, wait)
            if next_button:
                next_button.click()
                time.sleep(random.uniform(2, 4))
            else:
                break

        logging.info("All jobs sent to RabbitMQ queue")

        def callback(ch, method, properties, body):
            job = json.loads(body)
            apply_to_job(browser, job['id'], easy_applier, applied_jobs)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=JOB_QUEUE, on_message_callback=callback)

        logging.info("Waiting for jobs. To exit press CTRL+C")
        channel.start_consuming()

    except KeyboardInterrupt:
        logging.info("Interrupted by user, shutting down...")
    except Exception as e:
        if browser:
            save_screenshot_with_error(browser, f"An error occurred in main_mix: {str(e)}", "main_mix_error")
        logging.error(f"An error occurred in main_mix: {str(e)}")
    finally:
        if browser:
            browser.quit()
        if connection:
            connection.close()
        logging.debug("Browser session and RabbitMQ connection closed")

if __name__ == "__main__":
    main_mix()