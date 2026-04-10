from django.db import migrations


def seed_default_instruments(apps, schema_editor):
    Instrument = apps.get_model("tests", "Instrument")

    instruments = [
        {
            "code": "fdt",
            "name": "FDT - Five Digits Test",
            "category": "Funcoes executivas",
            "version": "1.0",
            "is_active": True,
        },
        {
            "code": "wisc4",
            "name": "WISC-IV - Escala de Inteligencia de Wechsler para Criancas",
            "category": "Inteligencia",
            "version": "4a Edicao",
            "is_active": True,
        },
        {
            "code": "bpa2",
            "name": "BPA-2 - Brief Psychological Assessment",
            "category": "Atencao",
            "version": "2a Edicao",
            "is_active": True,
        },
        {
            "code": "ebadep_a",
            "name": "EBADEP-A - Escala Brasileira de Avaliacao de Deficits de Atencao e Hiperatividade - Adulto",
            "category": "TDAH",
            "version": "1.0",
            "is_active": True,
        },
        {
            "code": "ebadep_ij",
            "name": "EBADEP-IJ - Escala Brasileira de Avaliacao de Deficits de Atencao e Hiperatividade - Infantojuvenil",
            "category": "TDAH",
            "version": "1.0",
            "is_active": True,
        },
        {
            "code": "epq_j",
            "name": "EPQ-J - Questionario de Personalidade para Criancas e Adolescentes",
            "category": "Personalidade",
            "version": "1.0",
            "is_active": True,
        },
        {
            "code": "etdah_ad",
            "name": "ETDAH-AD - Escala de Transtorno de Deficit de Atencao e Hiperatividade - Adulto",
            "category": "TDAH",
            "version": "1.0",
            "is_active": True,
        },
        {
            "code": "etdah_pais",
            "name": "ETDAH-PAIS - Escala de Transtorno de Deficit de Atencao e Hiperatividade - Versao para Pais",
            "category": "TDAH",
            "version": "1.0",
            "is_active": True,
        },
        {
            "code": "scared",
            "name": "SCARED - Screen for Child Anxiety Related Emotional Disorders",
            "category": "Ansiedade",
            "version": "1.0",
            "is_active": True,
        },
        {
            "code": "ravlt",
            "name": "RAVLT - Rey Auditory Verbal Learning Test",
            "category": "Memoria",
            "version": "1.0",
            "is_active": True,
        },
        {
            "code": "srs2",
            "name": "SRS-2 - Social Responsiveness Scale",
            "category": "Social / Autismo",
            "version": "2.0",
            "is_active": True,
        },
    ]

    for item in instruments:
        Instrument.objects.update_or_create(code=item["code"], defaults=item)


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_default_instruments, migrations.RunPython.noop),
    ]
