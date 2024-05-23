"""Create a superuser for development.

This script takes the username, email, and password arguments from sys
argb. For it to work correctly it needs to run within the correct
context (django). So call it with:

$ python manage.py shell < create_superuser.py $USERNAME $EMAIL $PASSWORD
"""

from django.contrib.auth.models import User

USERNAME = "admin"
EMAIL = "admin@bgs.com"
PASSWORD = "admin"


def create_superuser(username, email, password):
    """Create a superuser."""
    try:
        # Check if the superuser already exists
        if User.objects.filter(username=username).exists():
            print(f"Superuser with username '{username}' already exists.")
            return

        # Create the superuser
        User.objects.create_superuser(username, email, password)
        print("Superuser created successfully.")
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error creating superuser: {e}")


create_superuser(USERNAME, EMAIL, PASSWORD)
