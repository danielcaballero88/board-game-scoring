#!/usr/bin/env bash

# The DJANGO_ENVIRONMENT environment variable is used to determine which
# settings file to use.
DJANGO_ENV='development' python manage.py runserver 0.0.0.0:8000
