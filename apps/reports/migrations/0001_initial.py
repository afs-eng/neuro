from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("evaluations", "0002_evaluationprogressentry"),
        ("patients", "0010_alter_patient_responsible_null"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Report",
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
                ("title", models.CharField(max_length=255, verbose_name="titulo")),
                (
                    "interested_party",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="interessado"
                    ),
                ),
                ("purpose", models.TextField(blank=True, verbose_name="finalidade")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Rascunho"),
                            ("generating", "Gerando"),
                            ("in_review", "Em revisao"),
                            ("finalized", "Finalizado"),
                            ("archived", "Arquivado"),
                        ],
                        default="draft",
                        max_length=30,
                        verbose_name="status",
                    ),
                ),
                (
                    "snapshot_payload",
                    models.JSONField(blank=True, default=dict, verbose_name="snapshot"),
                ),
                (
                    "final_text",
                    models.TextField(blank=True, verbose_name="texto final"),
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
                    "author",
                    models.ForeignKey(
                        on_delete=models.deletion.PROTECT,
                        related_name="reports",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="autor",
                    ),
                ),
                (
                    "evaluation",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="reports",
                        to="evaluations.evaluation",
                        verbose_name="avaliacao",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="reports",
                        to="patients.patient",
                        verbose_name="paciente",
                    ),
                ),
            ],
            options={
                "verbose_name": "Laudo",
                "verbose_name_plural": "Laudos",
                "ordering": ["-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="ReportSection",
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
                ("key", models.CharField(max_length=100, verbose_name="chave")),
                ("title", models.CharField(max_length=255, verbose_name="titulo")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="ordem")),
                (
                    "source_payload",
                    models.JSONField(
                        blank=True, default=dict, verbose_name="payload de origem"
                    ),
                ),
                (
                    "generated_text",
                    models.TextField(blank=True, verbose_name="texto gerado"),
                ),
                (
                    "edited_text",
                    models.TextField(blank=True, verbose_name="texto editado"),
                ),
                (
                    "is_locked",
                    models.BooleanField(default=False, verbose_name="bloqueado"),
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
                    "report",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="sections",
                        to="reports.report",
                        verbose_name="laudo",
                    ),
                ),
            ],
            options={
                "verbose_name": "Secao do laudo",
                "verbose_name_plural": "Secoes do laudo",
                "ordering": ["order", "id"],
                "unique_together": {("report", "key")},
            },
        ),
    ]
