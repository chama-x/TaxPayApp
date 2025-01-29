#!/usr/bin/env bash
# exit on error
set -o errexit

# Install python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p frontend/static/frontend/css media staticfiles

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate 