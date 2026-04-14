"""Management command to create an admin user from environment variables."""

import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create an admin user from environment variables"

    def handle(self, *args, **options):
        username = os.getenv("ADMIN_USERNAME", "admin")
        email = os.getenv("ADMIN_EMAIL", "admin@neuro.com")
        password = os.getenv("ADMIN_PASSWORD", "")
        full_name = os.getenv("ADMIN_FULL_NAME", "Administrador")

        if not password:
            raise CommandError(
                "ADMIN_PASSWORD environment variable is required"
            )

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f"Admin user '{username}' already exists. Skipping.")
            )
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            role="admin",
        )
        self.stdout.write(self.style.SUCCESS(f"Successfully created admin user '{username}'"))
