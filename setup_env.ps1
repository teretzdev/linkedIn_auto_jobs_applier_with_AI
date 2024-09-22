# Check if Python 3.12 is installed
$pythonVersion = py -3.12 --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python 3.12 is not installed or not accessible."
    Write-Host "Please ensure Python 3.12 is installed and accessible via 'py -3.12'."
    exit 1
}

Write-Host "Using Python version: $pythonVersion"

# Remove existing virtual environment if it exists
if (Test-Path "venv") {
    Write-Host "Removing existing virtual environment..."
    Remove-Item -Recurse -Force venv
}

# Create new virtual environment
Write-Host "Creating virtual environment..."
py -3.12 -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to create virtual environment."
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

# Verify activated environment
$activatedPythonVersion = python --version
Write-Host "Activated Python version: $activatedPythonVersion"

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
Write-Host "Installing requirements..."
pip install -r requirements.txt

Write-Host "Setup completed successfully!"
Write-Host "You are now in an activated virtual environment using Python $activatedPythonVersion"
Write-Host "To deactivate the environment, run: deactivate"