from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "full_name",
        "role",
        "is_staff",
        "is_active",
    )
    list_filter = ("role", "is_staff", "is_active", "is_superuser")
    search_fields = ("username", "email", "full_name", "crp")

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Informações profissionais",
            {
                "fields": (
                    "full_name",
                    "role",
                    "phone",
                    "crp",
                    "specialty",
                    "is_active_clinical",
                )
            },
        ),
    )