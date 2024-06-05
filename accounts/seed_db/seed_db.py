"""Script to seed the DB with account data.

Usage:
$ python manage.py shell < $PATH_TO_THIS_SCRIPT
"""

from .create_user import create_user
from .data import superusers, users

for user in users.values():
    is_superuser = user.username in superusers
    create_user(user["username"], user["email"], user["password"], is_superuser)
