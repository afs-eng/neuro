from django.conf import settings
from django.db import models

from apps.evaluations.models import Evaluation
from apps.patients.models import Patient


class ReportStatus(models.TextChoices):
    DRAFT = "draft", "Rascunho"
    GENERATING = "generating", "Gerando"
    IN_REVIEW = "in_review", "Em revisao"
    FINALIZED = "finalized", "Finalizado"
    ARCHIVED = "archived", "Arquivado"


class ReportQuerySet(models.QuerySet):
    def with_details(self):
        return self.select_related("evaluation", "patient", "author")


class Report(models.Model):
    evaluation = models.ForeignKey(
        Evaluation,
        on_delete=models.CASCADE,
        related_name="reports",
        verbose_name="avaliacao",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="reports",
        verbose_name="paciente",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="reports",
        verbose_name="autor",
    )
    title = models.CharField("titulo", max_length=255)
    interested_party = models.CharField("interessado", max_length=255, blank=True)
    purpose = models.TextField("finalidade", blank=True)
    status = models.CharField(
        "status",
        max_length=30,
        choices=ReportStatus.choices,
        default=ReportStatus.DRAFT,
    )
    snapshot_payload = models.JSONField("snapshot", default=dict, blank=True)
    final_text = models.TextField("texto final", blank=True)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Laudo"
        verbose_name_plural = "Laudos"

    objects = ReportQuerySet.as_manager()

    def __str__(self):
        return self.title


class ReportSection(models.Model):
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name="sections",
        verbose_name="laudo",
    )
    key = models.CharField("chave", max_length=100)
    title = models.CharField("titulo", max_length=255)
    order = models.PositiveIntegerField("ordem", default=0)
    source_payload = models.JSONField("payload de origem", default=dict, blank=True)
    generated_text = models.TextField("texto gerado", blank=True)
    edited_text = models.TextField("texto editado", blank=True)
    is_locked = models.BooleanField("bloqueado", default=False)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        unique_together = [("report", "key")]
        verbose_name = "Secao do laudo"
        verbose_name_plural = "Secoes do laudo"

    def __str__(self):
        return f"{self.report.title} - {self.title}"
