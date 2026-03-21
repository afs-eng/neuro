from django.conf import settings
from django.db import models

from apps.patients.models import Patient


class EvaluationStatus(models.TextChoices):
    DRAFT = "draft", "Rascunho"
    COLLECTING_DATA = "collecting_data", "Coletando dados"
    SCORING = "scoring", "Pontuando testes"
    WRITING = "writing", "Redigindo laudo"
    IN_REVIEW = "in_review", "Em revisão"
    APPROVED = "approved", "Aprovado"
    ARCHIVED = "archived", "Arquivado"


class Evaluation(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="evaluations",
        verbose_name="paciente",
    )
    examiner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="evaluations",
        verbose_name="profissional responsável",
    )
    referral_reason = models.TextField("motivo do encaminhamento", blank=True)
    evaluation_purpose = models.TextField("finalidade da avaliação", blank=True)
    start_date = models.DateField("data de início", null=True, blank=True)
    end_date = models.DateField("data de término", null=True, blank=True)
    status = models.CharField(
        "status",
        max_length=30,
        choices=EvaluationStatus.choices,
        default=EvaluationStatus.DRAFT,
    )
    general_notes = models.TextField("observações gerais", blank=True)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    def __str__(self):
        return f"{self.patient.full_name} - {self.get_status_display()}"