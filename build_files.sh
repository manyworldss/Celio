#!/bin/bash

set -e

echo "Starting build process..."

# Ensure python3.9 is available
if ! command -v python3.9 &> /dev/null
then
    echo "python3.9 could not be found"
    exit 1
fi

echo "Found python3.9"
echo "Path to python3.9: $(which python3.9)"

# Ensure pip is installed
python3.9 -m ensurepip --upgrade

echo "Installing dependencies from requirements.txt..."
python3.9 -m pip install -r requirements.txt

echo "Dependencies installed successfully. Listing installed packages:"
python3.9 -m pip freeze

echo "Running collectstatic..."
python3.9 manage.py collectstatic --noinput --clear

echo "collectstatic finished successfully."