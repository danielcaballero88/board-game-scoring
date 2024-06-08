#!/usr/bin/env bash

# Script to remove __pycache__ directories

# Change directory to root git repo path (Django project directory)
ROOT_DIR=$(git rev-parse --show-toplevel)
echo "Root directory of the Git repository: $ROOT_DIR"
cd $ROOT_DIR

# Remove __pycache__ directories, ignore `.venv` directory
find . -type d \( -name '.venv' -prune -o -name '__pycache__' \) | xargs rm -r
