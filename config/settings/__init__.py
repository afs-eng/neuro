import os


environment = os.getenv("DJANGO_ENV", "local").lower()

if environment == "production":
    from .production import *  # noqa: F401,F403
else:
    from .local import *  # noqa: F401,F403
