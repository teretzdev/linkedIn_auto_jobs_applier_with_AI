from utils import chromeBrowserOptions
from gpt import GPTAnswerer
from linkedIn_authenticator import LinkedInAuthenticator
from linkedIn_bot_facade import LinkedInBotFacade
from linkedIn_job_manager import LinkedInJobManager
from resume import Resume
from file_manager import FileManager
from config_validator import ConfigValidator, ConfigError
import re
from pathlib import Path
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from utils import chromeBrowserOptions
from gpt import GPTAnswerer
from linkedIn_authenticator import LinkedInAuthenticator
from linkedIn_bot_facade import LinkedInBotFacade
from linkedIn_job_manager import LinkedInJobManager
from resume import Resume

# ... (rest of the code remains the same)

def main():
    try:
        data_folder = Path("data_folder")
        secrets_file, config_file, plain_text_resume_file, _ = FileManager.validate_data_folder(data_folder)
        parameters = ConfigValidator.validate_config(config_file)
        email, password, gemini_api_key = ConfigValidator.validate_secrets(secrets_file)
        parameters['uploads'] = FileManager.file_paths_to_dict(None, plain_text_resume_file)
        parameters['outputFileDirectory'] = data_folder / 'output'

        create_and_run_bot(email, password, parameters, gemini_api_key)
    except (ConfigError, FileNotFoundError) as e:
        print(f"Configuration error: {e}")
        print("Refer to the configuration guide for troubleshooting: https://github.com/feder-cr/LinkedIn_AIHawk_automatic_job_application/blob/main/readme.md#configuration")
    except RuntimeError as e:
        print(f"Runtime error: {e}")
        print("Check browser setup and other runtime issues.")
        print("Refer to the configuration and troubleshooting guide: https://github.com/feder-cr/LinkedIn_AIHawk_automatic_job_application/blob/main/readme.md#configuration")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Refer to the general troubleshooting guide: https://github.com/feder-cr/LinkedIn_AIHawk_automatic_job_application/blob/main/readme.md#configuration")

if __name__ == "__main__":
    main()
