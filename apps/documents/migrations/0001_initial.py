from django.db import migrations, models

import apps.documents.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("evaluations", "0001_initial"),
        ("patients", "0010_alter_patient_responsible_null"),
    ]

    operations = [
        migrations.CreateModel(
            name="EvaluationDocument",
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
                    "file",
                    models.FileField(
                        upload_to=apps.documents.models.document_upload_to,
                        verbose_name="arquivo",
                    ),
                ),
                (
                    "document_type",
                    models.CharField(
                        choices=[
                            ("referral", "Encaminhamento"),
                            ("school_report", "Relatorio escolar"),
                            ("medical_report", "Relatorio medico"),
                            ("therapeutic_report", "Relatorio terapeutico"),
                            ("family_attachment", "Ficha/anexo da familia"),
                            ("school_activity", "Atividade escolar"),
                            ("exam", "Exame"),
                            ("form", "Formulario"),
                            ("exported_report", "Laudo exportado"),
                            ("other", "Outro"),
                        ],
                        default="other",
                        max_length=40,
                        verbose_name="tipo de documento",
                    ),
                ),
                (
                    "source",
                    models.CharField(blank=True, max_length=255, verbose_name="origem"),
                ),
                (
                    "document_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="data do documento"
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="observacoes")),
                (
                    "is_relevant_for_report",
                    models.BooleanField(
                        default=True, verbose_name="relevante para o laudo"
                    ),
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
                        related_name="documents",
                        to="evaluations.evaluation",
                        verbose_name="avaliacao",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="documents",
                        to="patients.patient",
                        verbose_name="paciente",
                    ),
                ),
            ],
            options={
                "verbose_name": "Documento da avaliacao",
                "verbose_name_plural": "Documentos da avaliacao",
                "ordering": ["-created_at"],
            },
        ),
    ]
