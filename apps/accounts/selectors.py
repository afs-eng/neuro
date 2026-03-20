from .models import User


def get_active_users():
    return User.objects.filter(is_active=True).order_by("full_name", "username")


def get_user_by_id(user_id: int):
    return User.objects.filter(id=user_id).first()