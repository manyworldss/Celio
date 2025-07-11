#!/bin/bash

set -e

echo "Starting build process..."

# Ensure python3.11 is available
if ! command -v python3.11 &> /dev/null
then
    echo "python3.11 could not be found"
    exit 1
fi

echo "Found python3.11"
echo "Path to python3.11: $(which python3.11)"

# Ensure pip is installed
python3.11 -m ensurepip --upgrade

echo "Installing dependencies from requirements.txt..."
python3.11 -m pip install -r requirements.txt

echo "Dependencies installed successfully. Listing installed packages:"
python3.11 -m pip freeze

echo "Running collectstatic..."
python3.11 manage.py collectstatic --noinput --clear

echo "collectstatic finished successfully."