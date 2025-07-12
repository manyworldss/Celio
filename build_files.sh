#!/bin/bash
set -e

echo "Starting build process..."

# Ensure python3 is available
if ! command -v python3 &> /dev/null
then
    echo "python3 could not be found"
    exit 1
fi

echo "Found python3"
echo "Path to python3: $(which python3)"

# Ensure pip is installed/upgraded
python3 -m ensurepip --upgrade

echo "Installing dependencies from requirements.txt..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "Dependencies installed successfully. Listing installed packages:"
python3 -m pip freeze

echo "Running collectstatic..."
python3 manage.py collectstatic --noinput --clear

echo "collectstatic finished successfully."

