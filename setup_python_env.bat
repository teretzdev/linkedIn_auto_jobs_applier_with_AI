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

echo Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

echo Verifying activated environment...
python --version
if %errorlevel% neq 0 (
    echo Failed to verify activated environment.
    pause
    exit /b 1
)

echo Upgrading pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo Failed to upgrade pip.
    pause
    exit /b 1
)

echo Installing requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install requirements.
    pause
    exit /b 1
)

echo Setup completed successfully!
echo You can now run your Python scripts using this virtual environment.
echo To activate this environment in the future, run: venv\Scripts\activate.bat
pause