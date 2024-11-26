@echo off
:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or has not been added to the PATH.
    pause
    exit /b
)

:: Install requirements.txt dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies from requirements.txt.
    pause
    exit /b
)

:: start the app.py
echo Starting the application...
python app.py
if %errorlevel% neq 0 (
    echo An error occurred while executing app.py
    pause
    exit /b
)

pause
