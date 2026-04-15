import base64
import hashlib
import hmac
import secrets
import struct
import time
import urllib.parse

from django.contrib.auth import get_user_model

from django.utils import timezone

from apps.accounts.models import (
    generate_api_token_id,
    hash_api_token,
    hash_two_factor_code,
)

User = get_user_model()


def create_user(*, username: str, email: str, password: str, **extra_fields):
    user = User(
        username=username,
        email=email,
        **extra_fields,
    )
    user.set_password(password)
    user.save()
    return user


def issue_api_token(user: User) -> str:
    raw_token = secrets.token_hex(32)
    user.api_token = generate_api_token_id()
    user.api_token_hash = hash_api_token(raw_token)
    user.save(update_fields=["api_token", "api_token_hash"])
    return raw_token


def generate_two_factor_secret() -> str:
    secret = secrets.token_bytes(20)
    return base64.b32encode(secret).decode("utf-8").rstrip("=")


def build_two_factor_uri(user: User, secret: str) -> str:
    label = urllib.parse.quote(f"NeuroAvalia:{user.email}")
    issuer = urllib.parse.quote("NeuroAvalia")
    return f"otpauth://totp/{label}?secret={secret.upper()}&issuer={issuer}&digits=6&period=30"


def _totp_code(secret: str, for_counter: int) -> str:
    padding = "=" * ((8 - (len(secret) % 8)) % 8)
    key = base64.b32decode((secret + padding).encode("utf-8"), casefold=True)
    counter = struct.pack(">Q", for_counter)
    digest = hmac.new(key, counter, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (
        ((digest[offset] & 0x7F) << 24)
        | ((digest[offset + 1] & 0xFF) << 16)
        | ((digest[offset + 2] & 0xFF) << 8)
        | (digest[offset + 3] & 0xFF)
    )
    return str(code % 1_000_000).zfill(6)


def verify_two_factor_code(secret: str, code: str, valid_window: int = 1) -> bool:
    if not secret or not code:
        return False

    code = code.strip().replace(" ", "")
    if not code.isdigit() or len(code) != 6:
        return False

    now = int(time.time()) // 30
    for offset in range(-valid_window, valid_window + 1):
        if _totp_code(secret, now + offset) == code:
            return True
    return False


def generate_backup_codes(count: int = 8) -> list[str]:
    return [secrets.token_hex(4) for _ in range(count)]


def hash_backup_codes(codes: list[str]) -> list[str]:
    return [hash_two_factor_code(code) for code in codes]


def confirm_two_factor_setup(
    user: User, secret: str, code: str
) -> tuple[bool, list[str]]:
    if not verify_two_factor_code(secret, code):
        return False, []

    backup_codes = generate_backup_codes()
    user.two_factor_secret = secret
    user.two_factor_enabled = True
    user.two_factor_backup_codes = hash_backup_codes(backup_codes)
    user.two_factor_confirmed_at = timezone.now()
    user.save(
        update_fields=[
            "two_factor_secret",
            "two_factor_enabled",
            "two_factor_backup_codes",
            "two_factor_confirmed_at",
        ]
    )
    return True, backup_codes


def verify_two_factor_login(user: User, code: str) -> bool:
    if verify_two_factor_code(user.two_factor_secret, code):
        return True

    if not user.two_factor_backup_codes:
        return False

    code_hash = hash_two_factor_code(code)
    remaining = [item for item in user.two_factor_backup_codes if item != code_hash]
    if len(remaining) == len(user.two_factor_backup_codes):
        return False

    user.two_factor_backup_codes = remaining
    user.save(update_fields=["two_factor_backup_codes"])
    return True


def update_user(user: User, **data):
    password = data.pop("password", None)

    for field, value in data.items():
        setattr(user, field, value)

    if password:
        user.set_password(password)

    if data.get("two_factor_enabled") is False:
        user.clear_two_factor_state()

    user.save()
    return user


def regenerate_api_token(user):
    return issue_api_token(user)
