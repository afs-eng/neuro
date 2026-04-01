FROM python:3.12-slim

# Evita gerar .pyc e permite que o python printe buffers rápido
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala ferramentas úteis e a biblioteca pg_isready para o entrypoint
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala UV (gerenciador de dependências hiper rápido)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copia e instala as bibliotecas primeiro (Cache layer)
COPY requirements.txt pyproject.toml uv.lock ./
RUN uv pip install --system -r requirements.txt

# Copia o projeto
COPY . .

# Dá permissão no entrypoint
RUN chmod +x /app/infra/docker/backend.entrypoint.sh

EXPOSE 8000

# Porta de entrada é o script que espera o DB e roda migrations
ENTRYPOINT ["/app/infra/docker/backend.entrypoint.sh"]

# CMD padrão para dev (pode ser subscrito via docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
