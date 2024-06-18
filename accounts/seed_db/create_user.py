import traceback

from django.contrib.auth import get_user_model


def create_user(username: str, email: str, password: str, superuser: bool = False):
    """Create a user."""
    User = get_user_model()
    try:
        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            print(f"User with username '{username}' already exists.")
            return

        # Create the superuser
        if superuser:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
        print("User created successfully.")
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Error creating user: {traceback.format_exc(exc)}")
