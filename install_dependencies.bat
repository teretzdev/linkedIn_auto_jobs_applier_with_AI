@echo off
echo Installing dependencies for LinkedIn Auto Jobs Applier...

pip install -e .
pip install webdriver-manager==4.0.2 --force-reinstall

echo Dependencies installed successfully!
echo You can now run the application with: python main.py
pause
