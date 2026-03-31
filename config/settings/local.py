from .base import *


DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:3000", "http://localhost:3000"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

LOGGING["root"]["level"] = "DEBUG"
