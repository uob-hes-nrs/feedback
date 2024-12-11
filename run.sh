#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")"
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt --upgrade > /dev/null
.venv/bin/python3 app.py
