from django.core.cache import cache
from ninja.errors import HttpError


def get_client_ip(request) -> str:
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def rate_limit(request, scope: str, limit: int, window_seconds: int) -> None:
    ip = get_client_ip(request)
    key = f"rate-limit:{scope}:{ip}"
    current = cache.get(key)

    if current is None:
        cache.set(key, 1, timeout=window_seconds)
        return

    if current >= limit:
        raise HttpError(429, "Muitas tentativas. Tente novamente em instantes.")

    try:
        cache.incr(key)
    except ValueError:
        cache.set(key, current + 1, timeout=window_seconds)
