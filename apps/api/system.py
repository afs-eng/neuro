from ninja import Router
from django.db import connection
from django.conf import settings
import os

router = Router(tags=["system"])

@router.get("/status")
def system_status(request):
    db_ok = False
    db_error = None
    tables = []
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_ok = True
            
            # Check if User table exists
            cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'")
            tables = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        db_error = str(e)

    return {
        "status": "online",
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
