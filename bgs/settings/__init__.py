import os

ENV = os.getenv("DJANGO_ENV")

# For the moment only development environment is supported, I need to
# add more environments as I create the configuration files for each one
# and deploy to different environments.
if ENV not in ("development",):
    raise ValueError(f"Invalid DJANGO_ENV: {ENV}")
else:
    from .default import *  # noqa: F403

if ENV == "development":
    from .development import *  # noqa: F403
