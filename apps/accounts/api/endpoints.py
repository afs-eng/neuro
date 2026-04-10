from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
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
    ForgotPasswordIn,
    ResetPasswordConfirmIn,
    RegisterIn,
    RegisterOut,
)


router = Router(tags=["accounts"])


@router.post("/login", response=LoginOut)
def login(request, payload: LoginIn):
    try:
        email = payload.email
        if not email:
            raise HttpError(400, "Informe o email")

        from django.contrib.auth import get_user_model

        User = get_user_model()

        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=payload.password)
        except User.DoesNotExist:
            user = None

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
                "full_name": user.full_name or user.get_full_name() or user.username,
                "display_name": user.display_name,
                "role": user.role,
                "sex": user.sex,
                "specialty": user.specialty,
            },
        }

    except Exception as e:
        import traceback

        print(f"🔥 Erro crítico no login: {str(e)}")
        print(traceback.format_exc())
        raise e


@router.post("/register", response={201: RegisterOut, 400: MessageOut})
def register(request, payload: RegisterIn):
    if User.objects.filter(email=payload.email).exists():
        return 400, {"message": "Email já cadastrado."}
    if User.objects.filter(username=payload.username).exists():
        return 400, {"message": "Nome de usuário já em uso."}

    if payload.crp and User.objects.filter(crp=payload.crp).exists():
        return 400, {"message": "CRP já vinculado a outro profissional."}

    user = create_user(**payload.dict())

    return 201, {
        "success": True,
        "message": "Usuário criado com sucesso.",
        "user": {
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
        },
    }


@router.post("/forgot-password", response=MessageOut)
def forgot_password(request, payload: ForgotPasswordIn):
    user = User.objects.filter(email=payload.email, is_active=True).first()

    if user:
        from django.core.mail import send_mail

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = (
            f"{getattr(settings, 'FRONTEND_BASE_URL', 'http://localhost:3000')}"
            f"/reset-password?uid={uid}&token={token}"
        )

        send_mail(
            subject="Redefinicao de senha - NeuroAvalia",
            message=(
                "Ola!\n\n"
                "Recebemos uma solicitacao para redefinir sua senha no NeuroAvalia.\n"
                f"Use este link para cadastrar uma nova senha:\n{reset_url}\n\n"
                "Se voce nao fez esta solicitacao, ignore este e-mail."
            ),
            from_email=getattr(
                settings, "DEFAULT_FROM_EMAIL", "no-reply@neuroavalia.local"
            ),
            recipient_list=[user.email],
            fail_silently=False,
        )

    return {
        "message": "Se o email estiver cadastrado, enviaremos as instrucoes para redefinir sua senha."
    }


@router.post("/reset-password/confirm", response={200: MessageOut, 400: MessageOut})
def reset_password_confirm(request, payload: ResetPasswordConfirmIn):
    try:
        user_id = urlsafe_base64_decode(payload.uid).decode()
        user = User.objects.get(pk=user_id, is_active=True)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        return 400, {"message": "Link invalido ou expirado."}

    if not default_token_generator.check_token(user, payload.token):
        return 400, {"message": "Link invalido ou expirado."}

    user.set_password(payload.password)
    user.save(update_fields=["password"])

    return {"message": "Senha redefinida com sucesso."}


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
