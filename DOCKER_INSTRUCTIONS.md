# ============================================================
# NeuroAvalia — Docker Compose Instructions
# ============================================================

## Desenvolvimento Local

```bash
# 1. Copie o arquivo de exemplo
cp .env.example .env

# 2. Suba todos os servicos
docker compose up --build

# 3. Rode as migracoes (primeira vez)
docker compose exec backend python manage.py migrate

# 4. Crie superusuario
docker compose exec backend python manage.py createsuperuser

# 5. Crie instrumentos de teste
docker compose exec backend python manage.py create_instruments
```

Apos iniciar:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api
- **Django Admin:** http://localhost:8000/admin
- **API Docs (Swagger):** http://localhost:8000/api/docs

## Producao Self-Hosted (VPS)

```bash
# 1. Copie o arquivo de exemplo
cp .env.example.prod .env.prod

# 2. Edite as variaveis de producao
nano .env.prod

# 3. Suba todos os servicos
docker compose -f docker-compose.prod.yml up -d --build

# 4. Rode as migracoes
docker compose -f docker-compose.prod.yml exec backend python manage.py migrate

# 5. Crie superusuario
docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

Apos iniciar em producao:
- **Frontend:** https://seu-dominio.com
- **Backend API:** https://api.seu-dominio.com/api
- **Django Admin:** https://api.seu-dominio.com/admin

## Comandos Uteis

```bash
# Ver logs
docker compose logs -f backend
docker compose logs -f frontend

# Parar servicos
docker compose down

# Parar e remover volumes (cuidado: apaga dados!)
docker compose down -v

# Reconstruir apenas um servico
docker compose up -d --build backend

# Executar comando no container
docker compose exec backend python manage.py shell
docker compose exec backend python manage.py test
```
