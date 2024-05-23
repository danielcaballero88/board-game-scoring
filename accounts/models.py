from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    """Custom user model for authentication.

    This is highly recommended by Django docs for new projects.
    https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project

    This user has email as unique identifier instead of username.
    """

    USERNAME_FIELD = "email"
    email = models.EmailField("Email address", unique=True)
    REQUIRED_FIELDS = []
