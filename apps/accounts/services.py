from django.contrib.auth import get_user_model
import secrets

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


def update_user(user: User, **data):
    password = data.pop("password", None)

    for field, value in data.items():
        setattr(user, field, value)

    if password:
        user.set_password(password)

    user.save()
    return user

def regenerate_api_token(user):
    user.api_token = secrets.token_hex(32)
    user.save(update_fields=['api_token'])
    return user 