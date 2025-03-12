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

---

## Additional Resources
- [GitHub Repository](https://github.com/feder-cr/LinkedIn_AIHawk_automatic_job_application)
- [Configuration Guide](https://github.com/feder-cr/LinkedIn_AIHawk_automatic_job_application/blob/main/readme.md#configuration)
- [Troubleshooting Guide](https://github.com/feder-cr/LinkedIn_AIHawk_automatic_job_application/blob/main/readme.md#troubleshooting)

---

## Support
For further assistance, please open an issue on the [GitHub repository](https://github.com/feder-cr/LinkedIn_AIHawk_automatic_job_application/issues).