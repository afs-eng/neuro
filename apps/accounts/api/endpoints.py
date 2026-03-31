from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from ninja import Router
from ninja.errors import HttpError
from ninja.security import django_auth
from apps.api.auth import bearer_auth


from apps.accounts.models import User
from apps.accounts.permissions import can_manage_users, can_view_users
from apps.accounts.selectors import get_active_users
from apps.accounts.services import create_user, update_user
from apps.accounts.services import regenerate_api_token

from .schemas import (
    ApiTokenOut,
    UserOut,
    MeOut,
    CreateUserIn,
    UpdateUserIn,
    MessageOut,
    LoginIn,
    LoginOut,
)


router = Router(tags=["accounts"])


@router.post("/login", response=LoginOut)
def login(request, payload: LoginIn):
    user = authenticate(username=payload.username, password=payload.password)
    if not user:
        raise HttpError(401, "Credenciais inválidas")
    if not user.is_active:
        raise HttpError(403, "Usuário inativo")
    return {
        "access": user.api_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.display_name,
            "role": user.role,
        },
    }


@router.get("/me", response=MeOut, auth=django_auth)
def me(request):
    user = request.user
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.display_name,
        "role": user.role,
        "is_superuser": user.is_superuser,
        "is_staff": user.is_staff,
        "is_active": user.is_active,
    }


@router.get("/users", response=list[UserOut], auth=django_auth)
def list_users(request):
    if not can_view_users(request):
        raise HttpError(403, "Você não tem permissão para listar usuários.")

    users = get_active_users()
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.display_name,
            "role": user.role,
            "phone": user.phone,
            "crp": user.crp,
            "specialty": user.specialty,
            "is_active": user.is_active,
            "is_active_clinical": user.is_active_clinical,
        }
        for user in users
    ]


@router.post("/users", response={201: UserOut, 403: MessageOut}, auth=django_auth)
def create_user_endpoint(request, payload: CreateUserIn):
    if not can_manage_users(request):
        return 403, {"message": "Você não tem permissão para criar usuários."}

    user = create_user(**payload.dict())

    return 201, {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.display_name,
        "role": user.role,
        "phone": user.phone,
        "crp": user.crp,
        "specialty": user.specialty,
        "is_active": user.is_active,
        "is_active_clinical": user.is_active_clinical,
    }


@router.patch(
    "/users/{user_id}", response={200: UserOut, 403: MessageOut}, auth=django_auth
)
def update_user_endpoint(request, user_id: int, payload: UpdateUserIn):
    if not can_manage_users(request):
        return 403, {"message": "Você não tem permissão para editar usuários."}

    user = get_object_or_404(User, id=user_id)
    cleaned_data = payload.dict(exclude_unset=True)
    user = update_user(user, **cleaned_data)

    return 200, {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.display_name,
        "role": user.role,
        "phone": user.phone,
        "crp": user.crp,
        "specialty": user.specialty,
        "is_active": user.is_active,
        "is_active_clinical": user.is_active_clinical,
    }


@router.get("/token", response=ApiTokenOut, auth=bearer_auth)
def get_api_token(request):
    return {"api_token": request.auth.api_token}


@router.post("/token/regenerate", response=ApiTokenOut, auth=bearer_auth)
def regenerate_token_endpoint(request):
    user = regenerate_api_token(request.auth)
    return {"api_token": user.api_token}
