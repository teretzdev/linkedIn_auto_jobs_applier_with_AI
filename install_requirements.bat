@echo on
setlocal enabledelayedexpansion

echo Checking if virtual environment is activated...
if not defined VIRTUAL_ENV (
    echo Virtual environment is not activated.
    echo Please run 'venv\Scripts\activate.bat' first, then run this script again.
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

echo Requirements installed successfully.
pause