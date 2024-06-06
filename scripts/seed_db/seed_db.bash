#!/usr/bin/env bash

# Script to seed the db with mock data

# Change directory to root git repo path (Django project directory)
ROOT_DIR=$(git rev-parse --show-toplevel)
echo "Root directory of the Git repository: $ROOT_DIR"
cd $ROOT_DIR

# Run the seed scripts for each app
# python manage.py shell < $ROOT_DIR/accounts/seed_db/seed_db.py
python manage.py shell < $ROOT_DIR/scoring/seed_db/seed_db.py
