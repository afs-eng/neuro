from django.conf import settings
from django.db import migrations, models

import apps.anamnesis.models


def seed_templates(apps, schema_editor):
    Template = apps.get_model("anamnesis", "AnamnesisTemplate")
    templates = [
        {
            "code": "anamnesis_child_v1",
            "name": "Anamnese Infantil",
            "target_type": "child",
            "version": "1.0",
            "schema_payload": {
                "intro": "Anamnese infantil destinada ao responsavel.",
                "sections": [
                    {
                        "key": "identificacao_responsavel",
                        "title": "Identificacao do responsavel",
                        "fields": [
                            {
                                "key": "submitted_by_name",
                                "label": "Seu nome",
                                "type": "text",
                                "required": True,
                            },
                            {
                                "key": "submitted_by_relation",
                                "label": "Parentesco com a crianca",
                                "type": "text",
                                "required": True,
                            },
                        ],
                    },
                    {
                        "key": "demanda",
                        "title": "Motivo da avaliacao",
                        "fields": [
                            {
                                "key": "main_complaint",
                                "label": "Qual a principal queixa ou demanda?",
                                "type": "textarea",
                                "required": True,
                            },
                            {
                                "key": "when_started",
                                "label": "Quando as dificuldades comecaram?",
                                "type": "textarea",
                                "required": False,
                            },
                        ],
                    },
                    {
                        "key": "desenvolvimento",
                        "title": "Desenvolvimento",
                        "fields": [
                            {
                                "key": "pregnancy_birth",
                                "label": "Houve intercorrencias na gestacao/parto?",
                                "type": "textarea",
                                "required": False,
                            },
                            {
                                "key": "development_milestones",
                                "label": "Marcos do desenvolvimento",
                                "type": "textarea",
                                "required": False,
                            },
                            {
                                "key": "health_history",
                                "label": "Historico de saude",
                                "type": "textarea",
                                "required": False,
                            },
                        ],
                    },
                    {
                        "key": "escola",
                        "title": "Escola e aprendizagem",
                        "fields": [
                            {
                                "key": "school_performance",
                                "label": "Como esta o desempenho escolar?",
                                "type": "textarea",
                                "required": False,
                            },
                            {
                                "key": "teacher_concerns",
                                "label": "Ha preocupacoes da escola/professores?",
                                "type": "textarea",
                                "required": False,
                            },
                        ],
                    },
                    {
                        "key": "comportamento",
                        "title": "Comportamento e rotina",
                        "fields": [
                            {
                                "key": "behavior_home",
                                "label": "Comportamento em casa",
                                "type": "textarea",
                                "required": False,
                            },
                            {
                                "key": "sleep_appetite",
                                "label": "Sono e alimentacao",
                                "type": "textarea",
                                "required": False,
                            },
                            {
                                "key": "strengths",
                                "label": "Pontos fortes da crianca",
                                "type": "textarea",
                                "required": False,
                            },
                        ],
                    },
                ],
            },
        },
        {
            "code": "anamnesis_adolescent_v1",
            "name": "Anamnese Adolescente",
            "target_type": "adolescent",
            "version": "1.0",
            "schema_payload": {
                "intro": "Anamnese para adolescente, podendo ser respondida pelo responsavel ou pelo proprio adolescente conforme orientacao clinica.",
                "sections": [
                    {
                        "key": "identificacao",
                        "title": "Identificacao",
                        "fields": [
                            {
                                "key": "submitted_by_name",
                                "label": "Nome de quem responde",
                                "type": "text",
                                "required": True,
                            },
                            {
                                "key": "submitted_by_relation",
                                "label": "Relacao com o adolescente",
                                "type": "text",
                                "required": True,
                            },
                        ],
                    },
                    {
                        "key": "demanda",
                        "title": "Demanda atual",
                        "fields": [
                            {
                                "key": "main_complaint",
                                "label": "Qual a principal demanda?",
                                "type": "textarea",
                                "required": True,
                            },
                            {
                                "key": "current_impacts",
                                "label": "Em quais areas isso impacta?",
                                "type": "textarea",
                                "required": False,
                            },
                        ],
                    },
                    {
                        "key": "historico_escolar",
                        "title": "Historico escolar",
                        "fields": [
                            {
                                "key": "school_history",
                                "label": "Como foi o percurso escolar?",
                                "type": "textarea",
                                "required": False,
                            },
                            {
                                "key": "learning_difficulties",
                                "label": "Houve dificuldades de aprendizagem?",
                                "type": "textarea",
                                "required": False,
                            },
                        ],
                    },
                    {
                        "key": "emocional_social",
                        "title": "Aspectos emocionais e sociais",
                        "fields": [
                            {
                                "key": "emotional_state",
                                "label": "Como percebe o estado emocional atual?",
                                "type": "textarea",
                                "required": False,
                            },
                            {
                                "key": "social_relationships",
                                "label": "Relacionamentos e convivencia social",
                                "type": "textarea",
                                "required": False,
                            },
                        ],
                    },
                    {
                        "key": "rotina",
                        "title": "Rotina",
                        "fields": [
                            {
                                "key": "sleep_routine",
                                "label": "Rotina de sono",
                                "type": "textarea",
                                "required": False,
                            },
                            {
                                "key": "screen_time",
                                "label": "Uso de telas",
                                "type": "textarea",
                                "required": False,
                            },
                            {
                                "key": "treatment_history",
                                "label": "Historico de acompanhamentos/tratamentos",
                                "type": "textarea",
                                "required": False,
                            },
                        ],
                    },
                ],
            },
        },
        {
            "code": "anamnesis_adult_v1",
            "name": "Anamnese Adulto",
            "target_type": "adult",
            "version": "1.0",
            "schema_payload": {
                "intro": "Anamnese para adulto, com foco em historia pessoal, demanda e funcionamento atual.",
                "sections": [
                    {
                        "key": "identificacao",
                        "title": "Identificacao",
                        "fields": [
                            {
                                "key": "submitted_by_name",
                                "label": "Nome de quem responde",
                                "type": "text",
                                "required": True,
                            },
                            {
                                "key": "submitted_by_relation",
                                "label": "Relacao com o paciente",
                                "type": "text",
                                "required": True,
                                "help_text": "Se for o proprio paciente, informe 'proprio paciente'.",
                            },
                        ],
                    },
                    {
                        "key": "demanda",
                        "title": "Demanda atual",
                        "fields": [
                            {
                                "key": "main_complaint",
                                "label": "Qual a principal queixa?",
                                "type": "textarea",
                                "required": True,
                            },
                            {
                                "key": "goals",
                                "label": "O que espera da avaliacao?",
                                "type": "textarea",
                                "required": False,
                            },
                        ],
                    },
                    {
                        "key": "historico_pessoal",
                        "title": "Historico pessoal e de saude",
                        "fields": [
                            {
                                "key": "medical_history",
                                "label": "Historico medico relevante",
                                "type": "textarea",
                                "required": False,
                            },
                            {
                                "key": "mental_health_history",
                                "label": "Historico de saude mental",
                                "type": "textarea",
                                "required": False,
                            },
                            {
                                "key": "medication",
                                "label": "Medicacoes em uso",
                                "type": "textarea",
                                "required": False,
                            },
                        ],
                    },
                    {
                        "key": "funcionamento_atual",
                        "title": "Funcionamento atual",
                        "fields": [
                            {
                                "key": "work_study",
                                "label": "Trabalho/estudo",
                                "type": "textarea",
                                "required": False,
                            },
                            {
                                "key": "memory_attention",
                                "label": "Queixas de memoria/atencao",
                                "type": "textarea",
                                "required": False,
                            },
                            {
                                "key": "daily_functioning",
                                "label": "Rotina e autonomia",
                                "type": "textarea",
                                "required": False,
                            },
                        ],
                    },
                    {
                        "key": "emocional",
                        "title": "Aspectos emocionais",
                        "fields": [
                            {
                                "key": "emotional_state",
                                "label": "Estado emocional atual",
                                "type": "textarea",
                                "required": False,
                            },
                            {
                                "key": "sleep_appetite",
                                "label": "Sono e alimentacao",
                                "type": "textarea",
                                "required": False,
                            },
                        ],
                    },
                ],
            },
        },
    ]
    for item in templates:
        Template.objects.get_or_create(code=item["code"], defaults=item)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0002_user_api_token"),
        ("evaluations", "0002_evaluationprogressentry"),
        ("patients", "0010_alter_patient_responsible_null"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AnamnesisTemplate",
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
                ("code", models.CharField(max_length=100, unique=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "target_type",
                    models.CharField(
                        choices=[
                            ("child", "Infantil"),
                            ("adolescent", "Adolescente"),
                            ("adult", "Adulto"),
                        ],
                        max_length=30,
                    ),
                ),
                ("version", models.CharField(default="1.0", max_length=20)),
                ("schema_payload", models.JSONField(blank=True, default=dict)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["name", "version"]},
        ),
        migrations.CreateModel(
            name="AnamnesisInvite",
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
                ("recipient_name", models.CharField(max_length=255)),
                ("recipient_email", models.EmailField(blank=True, max_length=254)),
                ("recipient_phone", models.CharField(blank=True, max_length=40)),
                (
                    "channel",
                    models.CharField(
                        choices=[("email", "E-mail"), ("whatsapp", "WhatsApp")],
                        max_length=20,
                    ),
                ),
                ("message", models.TextField(blank=True)),
                (
                    "token",
                    models.CharField(
                        default=apps.anamnesis.models.generate_invite_token,
                        max_length=255,
                        unique=True,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pendente"),
                            ("sent", "Enviado"),
                            ("opened", "Aberto"),
                            ("in_progress", "Em preenchimento"),
                            ("completed", "Concluido"),
                            ("expired", "Expirado"),
                            ("canceled", "Cancelado"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("sent_at", models.DateTimeField(blank=True, null=True)),
                ("opened_at", models.DateTimeField(blank=True, null=True)),
                ("last_activity_at", models.DateTimeField(blank=True, null=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("expires_at", models.DateTimeField(blank=True, null=True)),
                ("delivery_payload", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=models.deletion.PROTECT,
                        related_name="anamnesis_invites",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "evaluation",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="anamnesis_invites",
                        to="evaluations.evaluation",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="anamnesis_invites",
                        to="patients.patient",
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=models.deletion.PROTECT,
                        related_name="invites",
                        to="anamnesis.anamnesistemplate",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="AnamnesisResponse",
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
                ("answers_payload", models.JSONField(blank=True, default=dict)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Rascunho"),
                            ("submitted", "Enviado"),
                            ("reviewed", "Revisado"),
                        ],
                        default="draft",
                        max_length=20,
                    ),
                ),
                ("submitted_by_name", models.CharField(blank=True, max_length=255)),
                ("submitted_by_relation", models.CharField(blank=True, max_length=255)),
                ("submitted_at", models.DateTimeField(blank=True, null=True)),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "evaluation",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="anamnesis_responses",
                        to="evaluations.evaluation",
                    ),
                ),
                (
                    "invite",
                    models.OneToOneField(
                        on_delete=models.deletion.CASCADE,
                        related_name="response",
                        to="anamnesis.anamnesisinvite",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="anamnesis_responses",
                        to="patients.patient",
                    ),
                ),
                (
                    "reviewed_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=models.deletion.PROTECT,
                        related_name="reviewed_anamnesis_responses",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=models.deletion.PROTECT,
                        related_name="responses",
                        to="anamnesis.anamnesistemplate",
                    ),
                ),
            ],
            options={"ordering": ["-updated_at"]},
        ),
        migrations.RunPython(seed_templates, migrations.RunPython.noop),
    ]
