from pathlib import Path
import yaml

class FileManager:
    @staticmethod
    def validate_data_folder(data_folder):
        """
        Validates the data folder and returns the paths to the secrets file, config file, plain text resume file, and the output directory.
        """
        secrets_file = data_folder / "secrets.yaml"
        config_file = data_folder / "config.yaml"
        plain_text_resume_file = data_folder / "resume.txt"
        output_directory = data_folder / "output"

        if not all([secrets_file.exists(), config_file.exists(), plain_text_resume_file.exists()]):
            raise FileNotFoundError("One or more required files are missing in the data folder.")

        return secrets_file, config_file, plain_text_resume_file, output_directory

    @staticmethod
    def file_paths_to_dict(file_paths, plain_text_resume_file):
        """
        Converts file paths to a dictionary for use in the config file.
        """
        uploads = {}
        if file_paths is not None:
            for file_path in file_paths:
                file_name = Path(file_path).name
                uploads[file_name] = file_path
        uploads['resume'] = plain_text_resume_file
        return uploads

