#!/bin/bash

# Build the project
echo "Building the project..."
python3.11 -m pip install -r requirements.txt

echo "Collecting static files..."
python3.11 manage.py collectstatic --noinput --clear