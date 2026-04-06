from ninja import Router
from django.db import connection
from django.conf import settings
import os

router = Router(tags=["system"])

@router.get("/status")
def system_status(request, setup: bool = False):
    db_ok = False
    db_error = None
    tables = []
    setup_result = "Nenhum setup executado"
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_ok = True
            
            # Check if User table exists
            cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'")
            tables = [row[0] for row in cursor.fetchall()]

        # Setup logic if requested and DB connected
        if setup and db_ok:
            from django.contrib.auth import get_user_model
            from django.core.management import call_command
            
            User = get_user_model()
            
            # Force trigger migrations just in case
            try:
                call_command('migrate', interactive=False)
            except Exception as e:
                setup_result = f"Erro nas migrações: {str(e)}"
            
            # Create or update admin user
            user, created = User.objects.get_or_create(
                email="admin@neuroavalia.com",
                defaults={
                    "username": "admin",
                    "full_name": "Administrador do Sistema",
                    "role": "admin",
                    "is_superuser": True,
                    "is_staff": True
                }
            )
            user.set_password("Neuro@2026")
            user.save()
            
            if created:
                setup_result = "Usuário admin@neuroavalia.com CRIADO com sucesso! Senha: Neuro@2026"
            else:
                setup_result = "Usuário admin@neuroavalia.com ATUALIZADO com sucesso! Senha: Neuro@2026"

    except Exception as e:
        db_error = str(e)

    return {
        "status": "online",
        "setup_result": setup_result,
        "database": {
            "connected": db_ok,
            "error": db_error,
            "has_users_table": "accounts_user" in tables,
            "tables_count": len(tables)
        },
        "environment": {
            "debug": settings.DEBUG,
            "render_hostname": os.getenv("RENDER_EXTERNAL_HOSTNAME", "local"),
            "allowed_hosts": settings.ALLOWED_HOSTS
        }
    }
