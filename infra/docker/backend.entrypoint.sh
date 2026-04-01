#!/usr/bin/env bash
set -e

echo "[backend.entrypoint.sh] Iniciando verificacao do ambiente..."

# Espera inteligente usando o proprio gerenciador do Django para nao depender de variaveis divididas no sh
retries=30
while ! python manage.py check --database default > /dev/null 2>&1; do
    echo "⏳ Aguardando conexao com o banco de dados..."
    sleep 2
    retries=$((retries-1))
    if [ $retries -eq 0 ]; then
        echo "❌ Erro: Timeout ao aguardar inicializacao do banco de dados (Possivel configuracao incorreta das senhas DB)."
        exit 1
    fi
done

echo "✅ Banco de dados disponivel."

echo "🛠️ Rodando as Migrations do Django..."
python manage.py migrate --noinput

if [ "$DJANGO_ENV" = "production" ] || [ "$DJANGO_ENV" = "staging" ]; then
    echo "📦 Modo producao detectado: Correndo o collectstatic..."
    python manage.py collectstatic --noinput
fi

echo "🚀 Iniciando o comando base do container..."
exec "$@"
