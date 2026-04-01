from urllib.parse import urlparse

from .base import *


DEBUG = False


def _hostname_from_url(url: str) -> str:
    return urlparse(url).hostname or ""


def _append_unique(values: list[str], candidate: str) -> None:
    if candidate and candidate not in values:
        values.append(candidate)


render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME", "").strip()
backend_public_url = os.getenv("BACKEND_PUBLIC_URL", "").strip()
frontend_base_url = os.getenv("FRONTEND_BASE_URL", "").strip()

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS") or [
    "sistema-neuro.onrender.com",
    ".onrender.com",
]
_append_unique(ALLOWED_HOSTS, render_hostname)
_append_unique(ALLOWED_HOSTS, _hostname_from_url(backend_public_url))

CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")
if not CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = ["https://sistema-neuro.onrender.com"]
if render_hostname:
    _append_unique(CSRF_TRUSTED_ORIGINS, f"https://{render_hostname}")
if backend_public_url:
    _append_unique(CSRF_TRUSTED_ORIGINS, backend_public_url)

CORS_ALLOWED_ORIGINS = env_list("CORS_ALLOWED_ORIGINS")
if not CORS_ALLOWED_ORIGINS and frontend_base_url:
    CORS_ALLOWED_ORIGINS = [frontend_base_url]

SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DATABASES["default"] = dj_database_url.parse(
    os.getenv("DATABASE_URL", default_database_url),
    conn_max_age=600,
    ssl_require=env_bool("DATABASE_SSL_REQUIRE", True),
)

LOGGING["root"]["level"] = os.getenv("DJANGO_LOG_LEVEL", "INFO")
