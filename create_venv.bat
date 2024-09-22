@echo on
setlocal enabledelayedexpansion

echo Checking Python version...
py -3.12 --version
if %errorlevel% neq 0 (
    echo Python 3.12 is not installed or not accessible.
    echo Please ensure Python 3.12 is installed and accessible via 'py -3.12'.
    pause
    exit /b 1
)

echo Creating virtual environment...
py -3.12 -m venv venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)

echo Virtual environment created successfully.
echo To activate the environment, run: venv\Scripts\activate.bat
echo After activation, run install_requirements.bat to install the required packages.
pause