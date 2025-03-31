#!/bin/bash
pip install -r requirements.txt
playwright install
python messenger_bot.py
