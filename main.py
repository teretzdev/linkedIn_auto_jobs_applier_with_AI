from pathlib import Path
import yaml
from file_manager import FileManager

def main():
    data_folder = Path("./data")
    secrets_file, config_file, plain_text_resume_file, output_directory = FileManager.validate_data_folder(data_folder)