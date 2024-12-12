#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")"
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt --upgrade > /dev/null
source .venv/bin/activate
.venv/bin/python3 app.py