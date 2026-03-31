from django.db import models

from apps.evaluations.models import Evaluation
from apps.patients.models import Patient


class DocumentType(models.TextChoices):
    REFERRAL = "referral", "Encaminhamento"
    SCHOOL_REPORT = "school_report", "Relatorio escolar"
    MEDICAL_REPORT = "medical_report", "Relatorio medico"
    THERAPEUTIC_REPORT = "therapeutic_report", "Relatorio terapeutico"
    FAMILY_ATTACHMENT = "family_attachment", "Ficha/anexo da familia"
    SCHOOL_ACTIVITY = "school_activity", "Atividade escolar"
    EXAM = "exam", "Exame"
    FORM = "form", "Formulario"
    EXPORTED_REPORT = "exported_report", "Laudo exportado"
    OTHER = "other", "Outro"


def document_upload_to(instance, filename):
    evaluation_id = instance.evaluation_id or "sem-avaliacao"
    patient_id = instance.patient_id or "sem-paciente"
    return f"documents/patient_{patient_id}/evaluation_{evaluation_id}/{filename}"


class EvaluationDocumentQuerySet(models.QuerySet):
    def with_details(self):
        return self.select_related("evaluation", "patient")


class EvaluationDocument(models.Model):
    evaluation = models.ForeignKey(
        Evaluation,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="avaliacao",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="paciente",
    )
    title = models.CharField("titulo", max_length=255)
    file = models.FileField("arquivo", upload_to=document_upload_to)
    document_type = models.CharField(
        "tipo de documento",
        max_length=40,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
    )
    source = models.CharField("origem", max_length=255, blank=True)
    document_date = models.DateField("data do documento", null=True, blank=True)
    notes = models.TextField("observacoes", blank=True)
    is_relevant_for_report = models.BooleanField("relevante para o laudo", default=True)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Documento da avaliacao"
        verbose_name_plural = "Documentos da avaliacao"

    objects = EvaluationDocumentQuerySet.as_manager()

    def __str__(self):
        return f"{self.title} - {self.evaluation.code}"
