import os

from dotenv import load_dotenv

ENV = os.getenv("DJANGO_ENV")

# For the moment only development environment is supported, I need to
# add more environments as I create the configuration files for each one
# and deploy to different environments.
if ENV not in ("development",):
    raise ValueError(f"Invalid DJANGO_ENV: {ENV}")

# For development only, load the environment variables from .env file
# and do it before loading the default settings.
if ENV == "development":
    load_dotenv()
    print(".env file loaded successfully.")

# Load default settings.
from .default import *  # noqa: E402, F403

# Load specific settings for the environment (may override defaults).
if ENV == "development":
    from .development import *  # noqa: F403
