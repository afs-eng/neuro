from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("evaluations", "0001_initial"),
        ("patients", "0010_alter_patient_responsible_null"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="EvaluationProgressEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "entry_type",
                    models.CharField(
                        choices=[
                            ("anamnesis", "Anamnese"),
                            ("testing_session", "Sessao de testagem"),
                            ("scoring", "Correcao"),
                            ("feedback", "Devolutiva"),
                            ("family_contact", "Contato com familia"),
                            ("school_contact", "Contato com escola"),
                            ("clinical_meeting", "Reuniao clinica"),
                            ("other", "Outro"),
                        ],
                        default="other",
                        max_length=40,
                        verbose_name="tipo de evolucao",
                    ),
                ),
                ("entry_date", models.DateField(verbose_name="data da evolucao")),
                (
                    "start_time",
                    models.TimeField(
                        blank=True, null=True, verbose_name="hora inicial"
                    ),
                ),
                (
                    "end_time",
                    models.TimeField(blank=True, null=True, verbose_name="hora final"),
                ),
                ("objective", models.TextField(blank=True, verbose_name="objetivo")),
                (
                    "tests_applied",
                    models.TextField(blank=True, verbose_name="testes aplicados"),
                ),
                (
                    "observed_behavior",
                    models.TextField(
                        blank=True, verbose_name="comportamento observado"
                    ),
                ),
                (
                    "clinical_notes",
                    models.TextField(blank=True, verbose_name="notas clinicas"),
                ),
                (
                    "next_steps",
                    models.TextField(blank=True, verbose_name="proximos passos"),
                ),
                (
                    "include_in_report",
                    models.BooleanField(default=True, verbose_name="incluir no laudo"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="criado em"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="atualizado em"),
                ),
                (
                    "evaluation",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="progress_entries",
                        to="evaluations.evaluation",
                        verbose_name="avaliacao",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="evaluation_progress_entries",
                        to="patients.patient",
                        verbose_name="paciente",
                    ),
                ),
                (
                    "professional",
                    models.ForeignKey(
                        on_delete=models.deletion.PROTECT,
                        related_name="evaluation_progress_entries",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="profissional",
                    ),
                ),
            ],
            options={
                "verbose_name": "Evolucao da avaliacao",
                "verbose_name_plural": "Evolucoes da avaliacao",
                "ordering": ["-entry_date", "-created_at"],
            },
        ),
    ]
