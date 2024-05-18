#!/usr/bin/env bash

# Script to create Django superuser programmatically

# Change directory to your Django project directory
ROOT_DIR=$(git rev-parse --show-toplevel)
echo "Root directory of the Git repository: $ROOT_DIR"
cd $ROOT_DIR

# Run the Python script using manage.py shell
python manage.py shell < $ROOT_DIR/scripts/_create_superuser.py
