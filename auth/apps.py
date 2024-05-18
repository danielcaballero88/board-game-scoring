from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "auth"
    label = "dc_auth"  # Need to set a label to avoid an error with conflicting labels
