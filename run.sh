#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt --upgrade > /dev/null
python3 app.py
