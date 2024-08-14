import json
import os
import random
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
import glob
from webdriver_manager.chrome import ChromeDriverManager

# Updated import for Google Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts.chat import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain

headless = False
chromeProfilePath = os.path.join(os.getcwd(), "chrome_profile", "linkedin_profile")

def ensure_chrome_profile():
    profile_dir = os.path.dirname(chromeProfilePath)
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
    if not os.path.exists(chromeProfilePath):
        os.makedirs(chromeProfilePath)
    return chromeProfilePath

def is_scrollable(element):
    scroll_height = element.get_attribute("scrollHeight")
    client_height = element.get_attribute("clientHeight")
    return int(scroll_height) > int(client_height)

def scroll_slow(driver, scrollable_element, start=0, end=3600, step=100, reverse=False):
    if reverse:
        start, end = end, start
        step = -step
    if step == 0:
        raise ValueError("Step cannot be zero.")
    script_scroll_to = "arguments[0].scrollTop = arguments[1];"
    try:
        if scrollable_element.is_displayed():
            if not is_scrollable(scrollable_element):
                print("The element is not scrollable.")
                return
            if (step > 0 and start >= end) or (step < 0 and start <= end):
                print("No scrolling will occur due to incorrect start/end values.")
                return        
            for position in range(start, end, step):
                try:
                    driver.execute_script(script_scroll_to, scrollable_element, position)
                except Exception as e:
                    print(f"Error during scrolling: {e}")
                time.sleep(random.uniform(1.0, 2.6))
            driver.execute_script(script_scroll_to, scrollable_element, end)
            time.sleep(1)
        else:
            print("The element is not visible.")
    except Exception as e:
        print(f"Exception occurred: {e}")

def HTML_to_PDF(FilePath):
    # Validate and prepare file paths
    if not os.path.isfile(FilePath):
        raise FileNotFoundError(f"The specified file does not exist: {FilePath}")
    FilePath = f"file:///{os.path.abspath(FilePath).replace(os.sep, '/')}"
    
    # Using Gemini API to generate PDF
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.environ.get("GOOGLE_API_KEY"))

    with open(FilePath, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Use Gemini to generate a PDF from the HTML 
    prompt = ChatPromptTemplate.from_template(
        "Please convert the following HTML into a PDF format.\n\n{html}"
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    try:
        pdf_base64 = chain.run({"html": html_content})
        return pdf_base64

    except Exception as e:
        raise RuntimeError(f"Error generating PDF: {e}")

def chromeBrowserOptions():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--remote-debugging-port=9222')
    if headless:
        options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    # Ensure that the Chrome profile directory exists
    ensure_chrome_profile()

    if len(chromeProfilePath) > 0:
        initialPath = os.path.dirname(chromeProfilePath)
        profileDir = os.path.basename(chromeProfilePath)
        options.add_argument('--user-data-dir=' + initialPath)
        options.add_argument("--profile-directory=" + profileDir)
    else:
        options.add_argument("--incognito")
        
    return options

def printred(text):
    # ANSI color code for red
    RED = "\033[91m"
    RESET = "\033[0m"
    # Print the text in red
    print(f"{RED}{text}{RESET}")

def printyellow(text):
    # ANSI color code for yellow
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    # Print the text in yellow
    print(f"{YELLOW}{text}{RESET}")
