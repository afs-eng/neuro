from django.conf import settings
from django.db import migrations, models


def seed_templates_v2(apps, schema_editor):
    Template = apps.get_model("anamnesis", "AnamnesisTemplate")
    from apps.anamnesis.constants import get_default_templates

    for item in get_default_templates():
        Template.objects.update_or_create(
            code=item["code"],
            defaults={
                "name": item["name"],
                "target_type": item["target_type"],
                "version": item["version"],
                "schema_payload": item["schema_payload"],
                "is_active": True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("anamnesis", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="anamnesisresponse",
            name="invite",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="response",
                to="anamnesis.anamnesisinvite",
            ),
        ),
        migrations.AddField(
            model_name="anamnesisresponse",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.PROTECT,
                related_name="created_anamnesis_responses",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="anamnesisresponse",
            name="response_type",
            field=models.CharField(
                choices=[
                    ("child", "Infantil"),
                    ("adolescent", "Adolescente"),
                    ("adult", "Adulto"),
                ],
                default="adult",
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="anamnesisresponse",
            name="source",
            field=models.CharField(
                choices=[("internal", "Interno"), ("external", "Externo")],
                default="internal",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="anamnesisresponse",
            name="summary_payload",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.RunPython(seed_templates_v2, migrations.RunPython.noop),
    ]
