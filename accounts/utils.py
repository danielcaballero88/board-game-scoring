from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

User = get_user_model()


def get_user_by_email(email: str) -> AbstractUser | None:
    try:
        # TODO: optimize the query by indexing the email field.
        # (or is that already done by default by Django? note that I'm
        # using the default Django auth system with the provided tables)
        return User.objects.get(email=email)
    except ObjectDoesNotExist:
        return None
    except MultipleObjectsReturned:
        # TODO: Handle the case where multiple objects are returned
        # (this should never happen because email should be a unique
        # field so no user can register with an already used email)
        raise
