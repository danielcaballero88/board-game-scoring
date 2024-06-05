"""Script to seed the DB with account data.

Usage:
$ python manage.py shell < $PATH_TO_THIS_SCRIPT
"""

# It's important to use absolute imports because this will be run as a
# script from root directory from inside Django shell.
from accounts.seed_db.create_user import create_user
from accounts.seed_db.data import superusers, users


def seed_db():
    for user in users.values():
        print("Inserting user into DB:", user)
        is_superuser = user["username"] in superusers
        create_user(user["username"], user["email"], user["password"], is_superuser)


seed_db()
