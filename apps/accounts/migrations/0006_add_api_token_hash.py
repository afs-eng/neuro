from __future__ import annotations

import hashlib

from django.db import migrations, models


def forwards(apps, schema_editor):
    User = apps.get_model("accounts", "User")

    for user in User.objects.all().iterator():
        token = (user.api_token or "").strip()

        if token.startswith("tok_"):
            continue

        if not token:
            continue

        user.api_token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        user.api_token = f"tok_{hashlib.sha256(token.encode('utf-8')).hexdigest()[:16]}"
        user.save(update_fields=["api_token", "api_token_hash"])


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0005_user_sex"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="api_token_hash",
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
