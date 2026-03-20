from .models import UserRole


def is_authenticated(request) -> bool:
    return request.user.is_authenticated


def is_admin(request) -> bool:
    return request.user.is_authenticated and (
        request.user.is_superuser or request.user.role == UserRole.ADMIN
    )


def can_manage_users(request) -> bool:
    return is_admin(request)


def can_view_users(request) -> bool:
    return request.user.is_authenticated and request.user.role in {
        UserRole.ADMIN,
        UserRole.NEUROPSYCHOLOGIST,
        UserRole.REVIEWER,
    }