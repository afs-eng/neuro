import os


environment = os.getenv("DJANGO_ENV")
if environment:
    environment = environment.lower()
elif os.getenv("RENDER") or os.getenv("RENDER_EXTERNAL_HOSTNAME"):
    environment = "production"
else:
    environment = "local"

if environment == "production":
    from .production import *  # noqa: F401,F403
else:
    from .local import *  # noqa: F401,F403
