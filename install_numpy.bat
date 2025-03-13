@echo on
setlocal enabledelayedexpansion

echo Installing NumPy with minimal disk space usage...

:: Step 1: Check if Python is installed
echo Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python before running this script.
    pause
    exit /b 1
)

:: Step 2: Upgrade pip to the latest version
echo Upgrading pip to the latest version...
python -m pip install --upgrade pip --no-cache-dir
if %errorlevel% neq 0 (
    echo Failed to upgrade pip. Please check your Python installation.
    pause
    exit /b 1
)

:: Step 3: Install NumPy using pip with minimal cache usage
echo Installing NumPy...
python -m pip install numpy --no-cache-dir
if %errorlevel% neq 0 (
    echo Failed to install NumPy. Please check your internet connection or Python environment.
    pause
    exit /b 1
)

echo NumPy installed successfully.
pause
