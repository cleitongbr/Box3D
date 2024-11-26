#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed or has not been added to the PATH."
    exit 1
fi

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies from requirements.txt."
    exit 1
fi

# start the app.py
echo "Starting the application..."
python3 app.py
if [ $? -ne 0 ]; then
    echo "An error occurred while executing app.py."
    exit 1
fi

# Keep the terminal open
echo "Application closed. Press any key to continue..."
read -n 1
