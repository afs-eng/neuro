import os
import django

# Carrega o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# --- CONFIGURAÇÃO DO NOVO USUÁRIO ---
USERNAME = 'andre' # 👈 Troque pelo seu nome
EMAIL = 'andrealekhine@msn.com' # 👈 Troque pelo seu e-mail
PASSWORD = 'Jalove13' # 👈 Troque pela sua senha

def create_admin():
    if not User.objects.filter(username=USERNAME).exists():
        print(f"--- Criando Superusuário: {USERNAME} ---")
        User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        print("✅ Usuário criado com sucesso em produção!")
    else:
        print(f"⚠️ Aviso: Usuário '{USERNAME}' já existe.")

if __name__ == "__main__":
    create_admin()
