#!/usr/bin/env bash
# exit on error
set -o errexit

# ដំឡើង packages នានា
pip install -r requirements.txt

# ប្រមូលផ្តុំ Static files (WhiteNoise)
python manage.py collectstatic --no-input

# រត់ទិន្នន័យចូល Database
python manage.py migrate