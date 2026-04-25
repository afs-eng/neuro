from django.db import migrations


def add_wais3_instrument(apps, schema_editor):
    Instrument = apps.get_model("tests", "Instrument")
    Instrument.objects.update_or_create(
        code="wais3",
        defaults={
            "name": "WAIS-III - Escala de Inteligencia de Wechsler para Adultos",
            "category": "Inteligencia",
            "version": "3a Edicao",
            "is_active": True,
        },
    )


def remove_wais3_instrument(apps, schema_editor):
    Instrument = apps.get_model("tests", "Instrument")
    Instrument.objects.filter(code="wais3").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0002_seed_default_instruments"),
    ]

    operations = [
        migrations.RunPython(add_wais3_instrument, remove_wais3_instrument),
    ]
