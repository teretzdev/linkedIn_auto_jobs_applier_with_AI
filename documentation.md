# LinkedIn Bot Documentation

## Overview
This document provides detailed instructions for setting up and using the LinkedIn bot for automatic job applications. It also includes troubleshooting steps to resolve common issues.

---

## Setup Instructions

### Prerequisites
1. **Python**: Ensure Python 3.8 or higher is installed on your system.
2. **ChromeDriver**: Install ChromeDriver compatible with your Chrome browser version.
3. **Dependencies**: Install required Python packages using:
   ```bash
   pip install -r requirements.txt
   ```
   - If you encounter issues with `webdriver_manager`, ensure it is installed by running:
     ```bash
     pip install webdriver_manager
     ```

4. **RabbitMQ**: Ensure RabbitMQ is installed and running if using the job queue feature.

---

### Configuration
1. **Secrets File**:
   - Path: `data_folder/secrets.yaml`
   - Add your LinkedIn credentials and API keys:
     ```yaml
     email: your_email@example.com
     password: your_password
     openai_api_key: your_openai_api_key
     gemini_api_key: your_gemini_api_key
     ```

2. **Config File**:
   - Path: `data_folder/config.yaml`
   - Update job preferences, locations, and other parameters:
     ```yaml
     experienceLevel:
       entry: true
       associate: false
       mid: true
       senior: false
     ```

3. **Resume**:
   - Place your plain text resume in `data_folder/plain_text_resume.yaml`.

---

### Running the Bot
1. **Basic Run**:
   ```bash
   python main.py
   ```

2. **With Custom Resume**:
   ```bash
   python main.py --resume path/to/your/resume.pdf
   ```

3. **With Premade Resume**:
   ```bash
   python main.py --premade-resume path/to/premade/resume.pdf
   ```

---

## Dual Environment Setup

### Overview
This project requires both Python and Node.js environments to function correctly. Python is used for backend automation and data processing, while Node.js is utilized for frontend interactions and additional utilities. This dual setup ensures modularity and leverages the strengths of both ecosystems.

### Setting Up the Project
Follow these steps to set up the project:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/teretzdev/linkedIn_auto_jobs_applier_with_AI.git
   cd linkedIn_auto_jobs_applier_with_AI
   ```

2. **Python Environment**:
   - Ensure Python 3.8 or higher is installed.
   - Create and activate a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate.bat
     ```
   - Install Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Node.js Environment**:
   - Ensure Node.js and npm are installed.
   - Install Node.js dependencies:
     ```bash
     npm install
     ```

4. **Unified Setup Script**:
   - Alternatively, you can use the `setup.sh` script to automate the setup process:
     ```bash
     ./setup.sh
     ```
   - Ensure the Python virtual environment is activated before running the script.

5. **Configuration**:
   - Follow the instructions in the "Configuration" section below to set up necessary files like `secrets.yaml` and `config.yaml`.

---

## Troubleshooting

### Installation Methods

#### Method 1: Using pip with requirements.txt
```bash
pip install -r requirements.txt
```

#### Method 2: Using setup.py (Recommended)
```bash
pip install -e .
```

#### Method 3: For Windows Users
Run the included batch file:
```
install_dependencies.bat
```

### Troubleshooting webdriver_manager Issues

If you encounter the error `ModuleNotFoundError: No module named 'webdriver_manager'` after installation:

1. **Reinstall with force option**:
   ```bash
   pip install webdriver-manager==4.0.2 --force-reinstall
   ```

2. **Check Python Environment**:
   - Ensure you're using the same Python environment where you installed the dependencies
   - If using a virtual environment, make sure it's activated

3. **Path Issues**:
   - Sometimes Python can't find modules due to path issues. Try installing with:
   ```bash
   python -m pip install webdriver-manager==4.0.2
   ```

4. **Verify Installation**:
   ```bash
   python -c "import webdriver_manager; print(webdriver_manager.__version__)"
   ```
   This should print the version if installed correctly.

---

## Troubleshooting

### Common Issues
1. **Browser Initialization Failed**:
   - Ensure ChromeDriver is installed and compatible with your Chrome version.
   - Refer to the [browser setup guide](https://github.com/feder-cr/LinkedIn_AIHawk_automatic_job_application/blob/main/readme.md#browser-setup).

2. **Configuration Errors**:
   - Verify `config.yaml` and `secrets.yaml` are correctly formatted.
   - Check for missing or invalid fields.

3. **File Not Found**:
   - Ensure all required files (`config.yaml`, `secrets.yaml`, `plain_text_resume.yaml`) are present in the `data_folder`.

4. **Application Errors**:
   - Check logs for detailed error messages.
   - Ensure the bot has access to the LinkedIn job application pages.

5. **`webdriver_manager` Import Error**:
   - If you encounter an error related to `webdriver_manager`, ensure it is installed by running:
     ```bash
     pip install webdriver_manager
     ```
   - Verify that your Python environment is correctly set up and active.

---

## Additional Resources
- [GitHub Repository](https://github.com/feder-cr/LinkedIn_AIHawk_automatic_job_application)
- [Configuration Guide](https://github.com/feder-cr/LinkedIn_AIHawk_automatic_job_application/blob/main/readme.md#configuration)
- [Troubleshooting Guide](https://github.com/feder-cr/LinkedIn_AIHawk_automatic_job_application/blob/main/readme.md#troubleshooting)

---

## Support
For further assistance, please open an issue on the [GitHub repository](https://github.com/feder-cr/LinkedIn_AIHawk_automatic_job_application/issues).