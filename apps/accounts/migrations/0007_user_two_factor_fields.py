from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_add_api_token_hash"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="two_factor_backup_codes",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="user",
            name="two_factor_confirmed_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="two_factor_enabled",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="two_factor_secret",
            field=models.CharField(blank=True, default="", max_length=64),
        ),
    ]
