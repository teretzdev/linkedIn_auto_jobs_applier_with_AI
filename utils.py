import json
import os
import random
import time
import logging
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
import glob
from webdriver_manager.chrome import ChromeDriverManager
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def get_gemini_response(prompt):
    logging.debug(f"Generating response for prompt: {prompt}")
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(prompt)
        logging.debug(f"Received response: {response.text}")
        return response.text
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return None

# Remove the following import:
# from langchain_google_genai import ChatGoogleGenerativeAI

# Replace any usage of ChatGoogleGenerativeAI with get_gemini_response
# Example:
# chat = ChatGoogleGenerativeAI()
# response = chat.generate_response("Your prompt here")
# Becomes:
# response = get_gemini_response("Your prompt here")

headless = False
chromeProfilePath = os.path.join(os.getcwd(), "chrome_profile", "linkedin_profile")

def ensure_chrome_profile():
    profile_dir = os.path.dirname(chromeProfilePath)
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
        logging.debug(f"Created profile directory at {profile_dir}")
    if not os.path.exists(chromeProfilePath):
        os.makedirs(chromeProfilePath)
        logging.debug(f"Created Chrome profile at {chromeProfilePath}")
    return chromeProfilePath

def is_scrollable(element):
    scroll_height = element.get_attribute("scrollHeight")
    client_height = element.get_attribute("clientHeight")
    return int(scroll_height) > int(client_height)

def scroll_slow(driver, scrollable_element, start=0, end=3600, step=100, reverse=False):
    logging.debug(f"Starting scroll from {start} to {end} with step {step}, reverse={reverse}")
    if reverse:
        start, end = end, start
        step = -step
    if step == 0:
        logging.error("Step cannot be zero.")
        raise ValueError("Step cannot be zero.")
    script_scroll_to = "arguments[0].scrollTop = arguments[1];"
    try:
        if scrollable_element.is_displayed():
            if not is_scrollable(scrollable_element):
                logging.info("The element is not scrollable.")
                return
            if (step > 0 and start >= end) or (step < 0 and start <= end):
                logging.info("No scrolling will occur due to incorrect start/end values.")
                return
            for position in range(start, end, step):
                try:
                    driver.execute_script(script_scroll_to, scrollable_element, position)
                    logging.debug(f"Scrolled to position {position}")
                except WebDriverException as e:
                    logging.error(f"WebDriverException during scrolling to {position}: {e}")
                except Exception as e:
                    logging.error(f"Unexpected error during scrolling to {position}: {e}")
                time.sleep(random.uniform(1.0, 2.6))
            driver.execute_script(script_scroll_to, scrollable_element, end)
            logging.debug(f"Scrolled to end position {end}")
            time.sleep(1)
        else:
            logging.info("The element is not visible.")
    except Exception as e:
        logging.error(f"Exception during scrolling: {e}")

def chromeBrowserOptions():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Use relative path to avoid absolute path duplication
    try:
        options.add_argument(f"user-data-dir={os.path.join(os.getcwd(), 'chrome_profile', 'linkedin_profile')}")
        logging.debug(f"Chrome options set with user-data-dir={options.arguments[-1]}")
    except Exception as e:
        logging.error(f"Error setting Chrome options: {e}")
    return options

def printyellow(text: str) -> None:
    logging.warning(text)  # Using logging.warning for yellow-like output

