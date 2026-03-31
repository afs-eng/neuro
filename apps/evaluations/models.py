from django.conf import settings
from django.db import models

from apps.patients.models import Patient


class EvaluationStatus(models.TextChoices):
    DRAFT = "draft", "Rascunho"
    COLLECTING_DATA = "collecting_data", "Coletando dados"
    TESTS_IN_PROGRESS = "tests_in_progress", "Testes em andamento"
    SCORING = "scoring", "Pontuando testes"
    WRITING_REPORT = "writing_report", "Laudo em redação"
    IN_REVIEW = "in_review", "Em revisão"
    APPROVED = "approved", "Aprovado"
    ARCHIVED = "archived", "Arquivado"


class EvaluationPriority(models.TextChoices):
    LOW = "low", "Baixa"
    MEDIUM = "medium", "Média"
    HIGH = "high", "Alta"
    URGENT = "urgent", "Urgente"


class EvaluationEntryType(models.TextChoices):
    ANAMNESIS = "anamnesis", "Anamnese"
    TESTING_SESSION = "testing_session", "Sessao de testagem"
    SCORING = "scoring", "Correcao"
    FEEDBACK = "feedback", "Devolutiva"
    FAMILY_CONTACT = "family_contact", "Contato com familia"
    SCHOOL_CONTACT = "school_contact", "Contato com escola"
    CLINICAL_MEETING = "clinical_meeting", "Reuniao clinica"
    OTHER = "other", "Outro"


class EvaluationQuerySet(models.QuerySet):
    def with_details(self):
        return self.select_related("patient", "examiner")


class Evaluation(models.Model):
    title = models.CharField("título do caso", max_length=200, blank=True)
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
        null=True,
        blank=True,
    )
    referral_reason = models.TextField("motivo do encaminhamento", blank=True)
    evaluation_purpose = models.TextField("finalidade da avaliação", blank=True)
    clinical_hypothesis = models.TextField("hipótese clínica", blank=True)
    start_date = models.DateField("data de início", null=True, blank=True)
    end_date = models.DateField("data de término", null=True, blank=True)
    status = models.CharField(
        "status",
        max_length=30,
        choices=EvaluationStatus.choices,
        default=EvaluationStatus.DRAFT,
    )
    priority = models.CharField(
        "prioridade",
        max_length=20,
        choices=EvaluationPriority.choices,
        default=EvaluationPriority.MEDIUM,
    )
    is_archived = models.BooleanField("arquivado", default=False)
    closed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="closed_evaluations",
        verbose_name="encerrado por",
        null=True,
        blank=True,
    )
    closed_at = models.DateTimeField("encerrado em", null=True, blank=True)
    general_notes = models.TextField("observações gerais", blank=True)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    objects = EvaluationQuerySet.as_manager()

    def __str__(self):
        code = f"AV-{self.id:04d}"
        if self.title:
            return f"{code} - {self.title}"
        return f"{code} - {self.patient.full_name} - {self.get_status_display()}"

    @property
    def code(self):
        return f"AV-{self.id:04d}"


class EvaluationProgressEntryQuerySet(models.QuerySet):
    def with_details(self):
        return self.select_related("evaluation", "patient", "professional")


class EvaluationProgressEntry(models.Model):
    evaluation = models.ForeignKey(
        Evaluation,
        on_delete=models.CASCADE,
        related_name="progress_entries",
        verbose_name="avaliacao",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="evaluation_progress_entries",
        verbose_name="paciente",
    )
    professional = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="evaluation_progress_entries",
        verbose_name="profissional",
    )
    entry_type = models.CharField(
        "tipo de evolucao",
        max_length=40,
        choices=EvaluationEntryType.choices,
        default=EvaluationEntryType.OTHER,
    )
    entry_date = models.DateField("data da evolucao")
    start_time = models.TimeField("hora inicial", null=True, blank=True)
    end_time = models.TimeField("hora final", null=True, blank=True)
    objective = models.TextField("objetivo", blank=True)
    tests_applied = models.TextField("testes aplicados", blank=True)
    observed_behavior = models.TextField("comportamento observado", blank=True)
    clinical_notes = models.TextField("notas clinicas", blank=True)
    next_steps = models.TextField("proximos passos", blank=True)
    include_in_report = models.BooleanField("incluir no laudo", default=True)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        ordering = ["-entry_date", "-created_at"]
        verbose_name = "Evolucao da avaliacao"
        verbose_name_plural = "Evolucoes da avaliacao"

    objects = EvaluationProgressEntryQuerySet.as_manager()

    def __str__(self):
        return f"{self.evaluation.code} - {self.get_entry_type_display()} - {self.entry_date}"
