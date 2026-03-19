from .base import *

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INSTALLED_APPS += [
    # Ferramentas úteis em desenvolvimento
    # "django_extensions",
]

MIDDLEWARE += [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Em dev, pode usar SQLite se quiser testar rápido
if os.getenv("USE_SQLITE", "").lower() == "true":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Segurança relaxada para desenvolvimento
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# Logging mais verboso em dev
LOGGING["root"]["level"] = "DEBUG"