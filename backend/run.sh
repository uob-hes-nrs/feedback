#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")"
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt --upgrade
.venv/bin/python3 -m flask run
