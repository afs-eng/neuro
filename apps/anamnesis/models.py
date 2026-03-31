import secrets

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.evaluations.models import Evaluation
from apps.patients.models import Patient


def generate_invite_token() -> str:
    return secrets.token_urlsafe(32)


class AnamnesisTargetType(models.TextChoices):
    CHILD = "child", "Infantil"
    ADOLESCENT = "adolescent", "Adolescente"
    ADULT = "adult", "Adulto"


class AnamnesisChannel(models.TextChoices):
    EMAIL = "email", "E-mail"
    WHATSAPP = "whatsapp", "WhatsApp"


class AnamnesisInviteStatus(models.TextChoices):
    PENDING = "pending", "Pendente"
    SENT = "sent", "Enviado"
    OPENED = "opened", "Aberto"
    IN_PROGRESS = "in_progress", "Em preenchimento"
    COMPLETED = "completed", "Concluido"
    EXPIRED = "expired", "Expirado"
    CANCELED = "canceled", "Cancelado"


class AnamnesisResponseStatus(models.TextChoices):
    DRAFT = "draft", "Rascunho"
    SUBMITTED = "submitted", "Enviado"
    REVIEWED = "reviewed", "Revisado"


class AnamnesisResponseSource(models.TextChoices):
    INTERNAL = "internal", "Interno"
    EXTERNAL = "external", "Externo"


class AnamnesisTemplate(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    target_type = models.CharField(max_length=30, choices=AnamnesisTargetType.choices)
    version = models.CharField(max_length=20, default="1.0")
    schema_payload = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "version"]

    def __str__(self):
        return f"{self.name} ({self.version})"


class AnamnesisInviteQuerySet(models.QuerySet):
    def with_details(self):
        return self.select_related("evaluation", "patient", "template", "created_by")


class AnamnesisInvite(models.Model):
    evaluation = models.ForeignKey(
        Evaluation, on_delete=models.CASCADE, related_name="anamnesis_invites"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="anamnesis_invites"
    )
    template = models.ForeignKey(
        AnamnesisTemplate, on_delete=models.PROTECT, related_name="invites"
    )
    recipient_name = models.CharField(max_length=255)
    recipient_email = models.EmailField(blank=True)
    recipient_phone = models.CharField(max_length=40, blank=True)
    channel = models.CharField(max_length=20, choices=AnamnesisChannel.choices)
    message = models.TextField(blank=True)
    token = models.CharField(max_length=255, unique=True, default=generate_invite_token)
    status = models.CharField(
        max_length=20,
        choices=AnamnesisInviteStatus.choices,
        default=AnamnesisInviteStatus.PENDING,
    )
    sent_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    last_activity_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    delivery_payload = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="anamnesis_invites",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AnamnesisInviteQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.template.name} - {self.patient.full_name}"

    @property
    def is_expired(self) -> bool:
        return bool(self.expires_at and timezone.now() > self.expires_at)


class AnamnesisResponseQuerySet(models.QuerySet):
    def with_details(self):
        return self.select_related(
            "invite", "evaluation", "patient", "template", "reviewed_by", "created_by"
        )


class AnamnesisResponse(models.Model):
    invite = models.OneToOneField(
        AnamnesisInvite,
        on_delete=models.CASCADE,
        related_name="response",
        null=True,
        blank=True,
    )
    evaluation = models.ForeignKey(
        Evaluation, on_delete=models.CASCADE, related_name="anamnesis_responses"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="anamnesis_responses"
    )
    template = models.ForeignKey(
        AnamnesisTemplate, on_delete=models.PROTECT, related_name="responses"
    )
    response_type = models.CharField(
        max_length=30,
        choices=AnamnesisTargetType.choices,
        default=AnamnesisTargetType.ADULT,
    )
    source = models.CharField(
        max_length=20,
        choices=AnamnesisResponseSource.choices,
        default=AnamnesisResponseSource.INTERNAL,
    )
    answers_payload = models.JSONField(default=dict, blank=True)
    summary_payload = models.JSONField(default=dict, blank=True)
    status = models.CharField(
        max_length=20,
        choices=AnamnesisResponseStatus.choices,
        default=AnamnesisResponseStatus.DRAFT,
    )
    submitted_by_name = models.CharField(max_length=255, blank=True)
    submitted_by_relation = models.CharField(max_length=255, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="created_anamnesis_responses",
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="reviewed_anamnesis_responses",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AnamnesisResponseQuerySet.as_manager()

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Resposta - {self.patient.full_name} - {self.template.name}"
