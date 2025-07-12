#!/bin/bash

set -e

echo "Starting build process..."

# Ensure python is available
if ! command -v python &> /dev/null
then
    echo "python could not be found"
    exit 1
fi

echo "Found python"
echo "Path to python: $(which python)"
python --version

# Ensure pip is installed
python -m ensurepip --upgrade

echo "Installing dependencies from requirements.txt..."
python -m pip install -r requirements.txt

echo "Dependencies installed successfully. Listing installed packages:"
python -m pip freeze

echo "Running collectstatic..."
python manage.py collectstatic --noinput --clear

echo "collectstatic finished successfully."