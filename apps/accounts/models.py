from email.policy import default
from enum import unique
from annotated_types import MaxLen
from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets

from django.utils.html import MAX_URL_LENGTH 

class UserRole(models.TextChoices):
    ADMIN = "admin", "Administrador"
    NEUROPSYCHOLOGIST = "neuropsychologist", "Neuropsicólogo"
    ASSISTANT = "assistant", "Assistente"
    REVIEWER = "reviewer", "Revisor"
    READONLY = "readonly", "Somente leitura"

def generate_api_token():
    return secrets.token_hex(32)

class User(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True)
    role = models.CharField(
        max_length=30,
        choices=UserRole.choices,
        default=UserRole.ASSISTANT,
    )
    phone = models.CharField(max_length=30, blank=True)
    crp = models.CharField(max_length=50, blank=True)
    specialty = models.CharField(max_length=120, blank=True)
    is_active_clinical = models.BooleanField(default=True)
    api_token = models.CharField(
        max_length= 128,
        unique= True,
        default = generate_api_token,
    )
    
    def __str__(self):
        return self.display_name

    @property
    def display_name(self) -> str:
        return self.full_name or self.get_full_name() or self.username

    @property
    def can_manage_users(self) -> bool:
        return self.is_superuser or self.role == UserRole.ADMIN

    @property
    def can_approve_reports(self) -> bool:
        return self.role in {
            UserRole.ADMIN,
            UserRole.NEUROPSYCHOLOGIST,
            UserRole.REVIEWER,
        }