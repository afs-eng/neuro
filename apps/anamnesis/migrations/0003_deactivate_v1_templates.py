from django.db import migrations


def deactivate_v1_templates(apps, schema_editor):
    AnamnesisTemplate = apps.get_model("anamnesis", "AnamnesisTemplate")
    v1_codes = [
        "anamnesis_child_v1",
        "anamnesis_adolescent_v1",
        "anamnesis_adult_v1",
    ]
    AnamnesisTemplate.objects.filter(code__in=v1_codes).update(is_active=False)


def reactivate_v1_templates(apps, schema_editor):
    AnamnesisTemplate = apps.get_model("anamnesis", "AnamnesisTemplate")
    v1_codes = [
        "anamnesis_child_v1",
        "anamnesis_adolescent_v1",
        "anamnesis_adult_v1",
    ]
    AnamnesisTemplate.objects.filter(code__in=v1_codes).update(is_active=True)


class Migration(migrations.Migration):
    dependencies = [
        ("anamnesis", "0002_response_internal_fields_and_templates_v2"),
    ]

    operations = [
        migrations.RunPython(deactivate_v1_templates, reactivate_v1_templates),
    ]
