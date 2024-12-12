#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")"

# Load the .env file if it exists
source .env

# Set up Python environment
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt --upgrade > /dev/null

# Activate virtual environment
source .venv/bin/activate

# Run the application
.venv/bin/python3 app.py
