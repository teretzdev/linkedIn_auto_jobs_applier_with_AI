#!/bin/bash

# Unified setup script for Python and Node.js environments

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed
if ! command_exists python3; then
    echo "Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command_exists node; then
    echo "Node.js is not installed. Please install Node.js and try again."
    exit 1
fi

# Check if npm is installed
if ! command_exists npm; then
    echo "npm is not installed. Please install npm and try again."
    exit 1
fi

# Check if a Python virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Python virtual environment is not activated."
    echo "Creating and activating a virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "Failed to upgrade pip. Exiting."
    exit 1
fi

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies from requirements.txt..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install Python dependencies. Exiting."
        exit 1
    fi
else
    echo "requirements.txt not found. Skipping Python dependency installation."
fi

# Install Node.js dependencies
if [ -f "package.json" ]; then
    echo "Installing Node.js dependencies from package.json..."
    npm install
    if [ $? -ne 0 ]; then
        echo "Failed to install Node.js dependencies. Exiting."
        exit 1
    fi
else
    echo "package.json not found. Skipping Node.js dependency installation."
fi

echo "Setup completed successfully."