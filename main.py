import re
from pathlib import Path  # Added import for Path
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import click
import google.generativeai as genai
import logging
from selenium.webdriver.support.ui import WebDriverWait

from utils import chromeBrowserOptions, printyellow  # Ensure printyellow is imported
from linkedIn_authenticator import LinkedInAuthenticator
from linkedIn_bot_facade import LinkedInBotFacade
from linkedIn_job_manager import LinkedInJobManager
from resume import Resume
from gpt import GPTAnswerer  # Ensure GPTAnswerer is imported

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass

class GeminiAnswerer:
    def __init__(self, api_key: str):
        logging.debug("Initializing GeminiAnswerer")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        logging.debug("GeminiAnswerer initialized with model 'gemini-1.5-pro-latest'")

    def generate_answer(self, prompt: str) -> str:
        logging.debug(f"Generating answer for prompt: {prompt}")
        response = self.model.generate_content(prompt)
        logging.debug(f"Received response: {response.text}")
        return response.text

    def set_resume(self, resume):
        self.resume = resume

    def answer_question_textual_wide_range(self, question: str) -> str:
        prompt = f"Based on the resume information:
{self.resume}

Answer the following question: {question}"
        return self.generate_answer(prompt)

    def answer_question_numeric(self, question: str) -> str:
        prompt = f"Based on the resume information:
{self.resume}

Provide a numeric answer to the following question: {question}"
        return self.generate_answer(prompt)

    def answer_question_from_options(self, question: str, options: list) -> str:
        options_str = "
".join(f"- {option}" for option in options)
        prompt = f"Based on the resume information:
{self.resume}

Answer the following question by selecting the best option:
{question}

Options:
{options_str}"
        return self.generate_answer(prompt)

    def try_fix_answer(self, question: str, previous_answer: str, error_text: str) -> str:
        prompt = f"Based on the resume information:
{self.resume}

The following question was asked: {question}

The previous answer was: {previous_answer}

This resulted in an error: {error_text}

Please provide a corrected answer that addresses the error."
        return self.generate_answer(prompt)

    def get_resume_html(self) -> str:
        prompt = f"Based on the resume information:
{self.resume}

Generate an HTML version of this resume that is suitable for uploading to job application websites."
        return self.generate_answer(prompt)

class ConfigValidator:
    @staticmethod
    def validate_email(email: str) -> bool:
        logging.debug(f"Validating email: {email}")
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        valid = re.match(email_regex, email) is not None
        logging.debug(f"Email validation result: {valid}")
        return valid
    
    @staticmethod
    def validate_config(config_yaml_path: Path) -> dict:
        logging.debug(f"Validating config file at {config_yaml_path}")
        try:
            with open(config_yaml_path, 'r') as stream:
                parameters = yaml.safe_load(stream)
            logging.debug("Config file loaded successfully")
        except yaml.YAMLError as exc:
            logging.error(f"YAML error: {exc}")
            raise ConfigError(f"Error reading config file {config_yaml_path}: {exc}")
        except FileNotFoundError:
            logging.error(f"Config file not found: {config_yaml_path}")
            raise ConfigError(f"Config file not found: {config_yaml_path}")
        
        # Define valid experience levels
        valid_experience_levels = ['entry', 'associate', 'mid', 'senior', 'director', 'executive']
        experience_level = parameters.get('experienceLevel', {})  # Added line to define experience_level

        for level in valid_experience_levels:
            if level not in experience_level or not isinstance(experience_level[level], bool):
                logging.error(f"Experience level '{level}' must be a boolean value in config file {config_yaml_path}.")
                raise ConfigError(f"Experience level '{level}' must be a boolean value in config file {config_yaml_path}.")

        # Validate 'jobTypes'
        job_types = parameters.get('jobTypes', {})
        valid_job_types = [
            'full-time', 'contract', 'part-time', 'temporary', 'internship', 'other', 'volunteer'
        ]
        for job_type in valid_job_types:
            if job_type not in job_types or not isinstance(job_types[job_type], bool):
                logging.error(f"Job type '{job_type}' must be a boolean value in config file {config_yaml_path}.")
                raise ConfigError(f"Job type '{job_type}' must be a boolean value in config file {config_yaml_path}.")

        # Validate 'date'
        date = parameters.get('date', {})
        valid_dates = ['all time', 'month', 'week', '24 hours']
        for date_filter in valid_dates:
            if date_filter not in date or not isinstance(date[date_filter], bool):
                logging.error(f"Date filter '{date_filter}' must be a boolean value in config file {config_yaml_path}.")
                raise ConfigError(f"Date filter '{date_filter}' must be a boolean value in config file {config_yaml_path}.")

        # Validate 'positions'
        positions = parameters.get('positions', [])
        if not isinstance(positions, list) or not all(isinstance(pos, str) for pos in positions):
            logging.error(f"'positions' must be a list of strings in config file {config_yaml_path}.")
            raise ConfigError(f"'positions' must be a list of strings in config file {config_yaml_path}.")
        
        # Validate 'locations'
        locations = parameters.get('locations', [])
        if not isinstance(locations, list) or not all(isinstance(loc, str) for loc in locations):
            logging.error(f"'locations' must be a list of strings in config file {config_yaml_path}.")
            raise ConfigError(f"'locations' must be a list of strings in config file {config_yaml_path}.")

        # Validate 'distance'
        approved_distances = {0, 5, 10, 25, 50, 100}
        distance = parameters.get('distance')
        if distance not in approved_distances:
            logging.error(f"Invalid distance value in config file {config_yaml_path}. Must be one of: {approved_distances}")
            raise ConfigError(f"Invalid distance value in config file {config_yaml_path}. Must be one of: {approved_distances}")

        # Validate 'companyBlacklist'
        company_blacklist = parameters.get('companyBlacklist', [])
        if not isinstance(company_blacklist, list) or not all(isinstance(comp, str) for comp in company_blacklist):
            company_blacklist = []
        parameters['companyBlacklist'] = company_blacklist

        # Validate 'titleBlacklist'
        title_blacklist = parameters.get('titleBlacklist', [])
        if not isinstance(title_blacklist, list) or not all(isinstance(word, str) for word in title_blacklist):
            title_blacklist = []
        parameters['titleBlacklist'] = title_blacklist
        return parameters

    @staticmethod
    def validate_secrets(secrets_yaml_path: Path) -> tuple:
        logging.debug(f"Validating secrets file at {secrets_yaml_path}")
        try:
            with open(secrets_yaml_path, 'r') as stream:
                secrets = yaml.safe_load(stream)
            logging.debug("Secrets file loaded successfully")
        except yaml.YAMLError as exc:
            logging.error(f"YAML error: {exc}")
            raise ConfigError(f"Error reading secrets file {secrets_yaml_path}: {exc}")
        except FileNotFoundError:
            logging.error(f"Secrets file not found: {secrets_yaml_path}")
            raise ConfigError(f"Secrets file not found: {secrets_yaml_path}")

        mandatory_secrets = ['email', 'password', 'gemini_api_key']

        for secret in mandatory_secrets:
            if secret not in secrets:
                logging.error(f"Missing secret: {secret}")
                raise ConfigError(f"Missing secret in file {secrets_yaml_path}: {secret}")
           
        if not ConfigValidator.validate_email(secrets['email']):
            logging.error("Invalid email format")
            raise ConfigError(f"Invalid email format in secrets file {secrets_yaml_path}.")
        if not secrets['password']:
            logging.error("Password is empty")
            raise ConfigError("Password cannot be empty in secrets file.")
        if not secrets['gemini_api_key']:
            logging.error("Gemini API key is empty")
            raise ConfigError("Gemini API key cannot be empty in secrets file.")

        logging.debug("Secrets validated successfully")
        return secrets['email'], str(secrets['password']), secrets['gemini_api_key']

class FileManager:
    @staticmethod
    def find_file(name_containing: str, with_extension: str, at_path: Path) -> Path:
        logging.debug(f"Searching for file containing '{name_containing}' with extension '{with_extension}' in {at_path}")
        for file in at_path.iterdir():
            if name_containing.lower() in file.name.lower() and file.suffix.lower() == with_extension.lower():
                logging.debug(f"Found file: {file}")
                return file
        logging.warning(f"No file found containing '{name_containing}' with extension '{with_extension}' in {at_path}")
        return None

    @staticmethod
    def validate_data_folder(app_data_folder: Path) -> tuple:
        logging.debug(f"Validating data folder at {app_data_folder}")
        if not app_data_folder.exists() or not app_data_folder.is_dir():
            logging.error(f"Data folder not found: {app_data_folder}")
            raise FileNotFoundError(f"Data folder not found: {app_data_folder}")

        secrets_file = app_data_folder / 'secrets.yaml'
        config_file = app_data_folder / 'config.yaml'
        plain_text_resume_file = app_data_folder / 'plain_text_resume.yaml'
        
        missing_files = []
        if not config_file.exists():
            missing_files.append('config.yaml')
        if not plain_text_resume_file.exists():
            missing_files.append('plain_text_resume.yaml')
        
        if missing_files:
            logging.error(f"Missing files in the data folder: {', '.join(missing_files)}")
            raise FileNotFoundError(f"Missing files in the data folder: {', '.join(missing_files)}")
        
        output_folder = app_data_folder / 'output'
        output_folder.mkdir(exist_ok=True)
        logging.debug(f"Output folder is set to {output_folder}")
        return secrets_file, config_file, plain_text_resume_file, output_folder

    @staticmethod
    def file_paths_to_dict(resume_file: Path | None, plain_text_resume_file: Path) -> dict:
        logging.debug("Converting file paths to dictionary")
        if not plain_text_resume_file.exists():
            logging.error(f"Plain text resume file not found: {plain_text_resume_file}")
            raise FileNotFoundError(f"Plain text resume file not found: {plain_text_resume_file}")
        
        result = {'plainTextResume': plain_text_resume_file}
        
        if resume_file is not None:
            if not resume_file.exists():
                logging.error(f"Resume file not found: {resume_file}")
                raise FileNotFoundError(f"Resume file not found: {resume_file}")
            result['resume'] = resume_file
            logging.debug(f"Added resume file to dictionary: {resume_file}")
        
        logging.debug("File paths conversion successful")
        return result

def init_browser():
    logging.debug("Initializing browser")
    try:
        options = chromeBrowserOptions()
        service = ChromeService(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)
        logging.info("Browser initialized successfully")
        return browser
    except Exception as e:
        logging.error(f"Failed to initialize browser: {str(e)}")
        raise RuntimeError(f"Failed to initialize browser: {str(e)}")

def create_and_run_bot(email: str, password: str, parameters: dict, gemini_api_key: str):
    logging.debug("Creating and running the bot")
    try:
        browser = init_browser()
        wait = WebDriverWait(browser, 10)
        
        # Initialize GPTAnswerer with correct API keys
        gpt_answerer_component = GPTAnswerer(
            openai_api_key=parameters.get('openai_api_key', ''),
            google_api_key=gemini_api_key
        )
        logging.debug("GPTAnswerer initialized with provided API keys")
        
        login_component = LinkedInAuthenticator(browser)
        logging.debug("LinkedInAuthenticator initialized")
        
        apply_component = LinkedInJobManager(browser, wait)
        logging.debug("LinkedInJobManager initialized")
        
        # Set gpt_answerer using the setter method
        apply_component.set_gpt_answerer(gpt_answerer_component)
        logging.debug("GPTAnswerer set in LinkedInJobManager")
        
        with open(parameters['uploads']['plainTextResume'], "r") as file:
            plain_text_resume_file = file.read()
        resume_object = Resume(plain_text_resume_file)
        logging.debug("Resume object created")
        
        # Initialize LinkedInBotFacade with all components
        bot = LinkedInBotFacade(login_component, apply_component, browser)
        logging.debug("LinkedInBotFacade initialized")
        
        bot.set_secrets(email, password)
        bot.set_resume(resume_object)
        bot.set_gemini_answerer(gpt_answerer_component)
        bot.set_parameters(parameters)
        logging.debug("Bot parameters set")
        
        bot.start_login()
        logging.info("Bot started login process")
        
        bot.start_apply()
        logging.info("Bot started application process")
    except Exception as e:
        logging.error(f"Error running the bot: {str(e)}")
        raise RuntimeError(f"Error running the bot: {str(e)}")

@click.command()
@click.option('--resume', type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path), help="Path to the resume PDF file")
def main(resume: Path = None):
    logging.debug("Main function started")
    try:
        data_folder = Path("data_folder")
        secrets_file, config_file, plain_text_resume_file, output_folder = FileManager.validate_data_folder(data_folder)
        logging.debug("Data folder validated")
        
        parameters = ConfigValidator.validate_config(config_file)
        logging.debug("Configuration validated")
        
        email, password, gemini_api_key = ConfigValidator.validate_secrets(secrets_file)
        logging.debug("Secrets validated")
        
        parameters['uploads'] = FileManager.file_paths_to_dict(resume, plain_text_resume_file)
        parameters['outputFileDirectory'] = output_folder
        logging.debug("File paths set in parameters")

        create_and_run_bot(email, password, parameters, gemini_api_key)
        logging.info("Bot execution completed successfully")
    except ConfigError as ce:
        logging.error(f"Configuration error: {str(ce)}")
        printyellow("Configuration error occurred. Please check the logs for details.")
        printyellow("Refer to the configuration guide for troubleshooting: https://github.com/feder-cr/LinkedIn_AIHawk_automatic_job_application/blob/main/readme.md#configuration")
    except FileNotFoundError as fnf:
        logging.error(f"File not found: {str(fnf)}")
        printyellow("File not found error. Please check the logs for details.")
        printyellow("Ensure all required files are present in the data folder.")
        printyellow("Refer to the file setup guide: https://github.com/feder-cr/LinkedIn_AIHawk_automatic_job_application/blob/main/readme.md#configuration")
    except RuntimeError as re:
        logging.error(f"Runtime error: {str(re)}")
        printyellow("Runtime error occurred. Please check the logs for details.")
        printyellow("Check browser setup and other runtime issues.")
        printyellow("Refer to the configuration and troubleshooting guide: https://github.com/feder-cr/LinkedIn_AIHawk_automatic_job_application/blob/main/readme.md#configuration")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        printyellow("An unexpected error occurred. Please check the logs for details.")
        printyellow("Refer to the general troubleshooting guide: https://github.com/feder-cr/LinkedIn_AIHawk_automatic_job_application/blob/main/readme.md#configuration")

if __name__ == "__main__":
    logging.debug("Starting the application")
    main()

