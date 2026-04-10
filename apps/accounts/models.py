from django.contrib.auth.models import AbstractUser

from django.db import models
import secrets


class UserRole(models.TextChoices):
    ADMIN = "admin", "Administrador"
    NEUROPSYCHOLOGIST = "neuropsychologist", "Neuropsicólogo"
    ASSISTANT = "assistant", "Assistente"
    REVIEWER = "reviewer", "Revisor"
    READONLY = "readonly", "Somente leitura"


def generate_api_token():
    return secrets.token_hex(32)


class User(AbstractUser):
    email = models.EmailField(unique=True)

    full_name = models.CharField(max_length=255, blank=True)
    role = models.CharField(
        max_length=30,
        choices=UserRole.choices,
        default=UserRole.ASSISTANT,
    )
    SEX_CHOICES = [
        ("M", "Masculino"),
        ("F", "Feminino"),
        ("O", "Outro"),
    ]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default="M")
    phone = models.CharField(max_length=30, blank=True)

    crp = models.CharField(max_length=50, blank=True, unique=True, null=True)



    specialty = models.CharField(max_length=120, blank=True)
    is_active_clinical = models.BooleanField(default=True)
    api_token = models.CharField(
        max_length=128,
        unique=True,
        default=generate_api_token,
    )

    def __str__(self):
        return self.display_name

    @property
    def display_name(self) -> str:
        # Get only the first name
        name_parts = (self.full_name or self.username).split()
        first_name = name_parts[0] if name_parts else self.username

        # Clean name from existing Dr/Dra (case insensitive)
        clean_name = first_name.replace("Dr.", "").replace("Dra.", "").replace("Dr", "").replace("Dra", "").strip()

        prefix = "Dra. " if self.sex == "F" else "Dr. "
        return f"{prefix}{clean_name}"


    @property
    def initials(self) -> str:
        if self.full_name:
            parts = self.full_name.split()
            if len(parts) >= 2:
                return f"{parts[0][0]}{parts[-1][0]}".upper()
            return parts[0][:2].upper()
        return self.username[:2].upper()


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
