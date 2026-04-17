# Deploy de Teste - NeuroAvalia

## Visao Geral

- Frontend: Vercel
- Backend: Render Web Service
- Banco: PostgreSQL no Render

---

## Backend no Render

### Criar servico

- Tipo: `Web Service`
- Runtime: `Python`
- Root directory: raiz do repositorio

### Build command

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

### Pre-deploy command

```bash
python manage.py migrate
```

### Start command

```bash
gunicorn config.wsgi:application --log-file -
```

### Health check

- Path: `/healthz/`

### Variaveis de ambiente do backend

- `DJANGO_ENV=production`
- `DEBUG=False`
- `SECRET_KEY=<gerada>`
- `DATABASE_URL=<connection string do PostgreSQL do Render>`
- `DATABASE_SSL_REQUIRE=True`
- `ALLOWED_HOSTS=<dominio-do-render>`
- `CSRF_TRUSTED_ORIGINS=https://<dominio-render>,https://<dominio-vercel>`
- `CORS_ALLOWED_ORIGINS=https://<dominio-vercel>`
- `FRONTEND_BASE_URL=https://<dominio-vercel>`
- `BACKEND_PUBLIC_URL=https://<dominio-render>`
- `ALLOW_VERCEL_PREVIEWS=True`
- `AI_PROVIDER=openai`
- `OPENAI_API_KEY=<chave-openrouter>`
- `OPENAI_BASE_URL=https://openrouter.ai/api/v1`
- `OPENAI_REFERER=https://<dominio-vercel>`
- `OPENAI_TITLE=NeuroAvalia`
- `OPENAI_MODEL_TEXT=google/gemma-4-31b-it:free`
- `OPENAI_MODEL_REASONING=google/gemma-4-31b-it:free`
- `OPENAI_FALLBACK_MODELS=google/gemma-3-27b-it:free,meta-llama/llama-3.3-70b-instruct:free,openai/gpt-oss-20b:free`
- `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL`
- `DJANGO_LOG_LEVEL=INFO`

### Banco PostgreSQL

- Crie um `PostgreSQL` no Render
- Copie a connection string para `DATABASE_URL`

---

## Frontend no Vercel

### Projeto

- Framework: `Next.js`
- Root directory: `neuro-frontend`

### Variaveis de ambiente do frontend

- `NEXT_PUBLIC_API_BASE_URL=https://<dominio-render>`
- `INTERNAL_API_BASE_URL=https://<dominio-render>`
- `NEXT_PUBLIC_APP_URL=https://<dominio-vercel>`

### Observacoes

- O frontend consome a API publica do Render
- As variaveis do frontend devem apontar para a raiz do backend, sem adicionar `/api` no final
- As rotas publicas de anamnese por token usam a URL do frontend em `FRONTEND_BASE_URL`
- O OpenRouter fica configurado apenas no backend do Render; nenhuma chave de IA deve ir para o Vercel

---

## Checklist Final

- Backend responde em `/healthz/`
- Frontend consegue autenticar e listar dados
- Migrations aplicadas no PostgreSQL
- Arquivos estaticos coletados com sucesso
- Upload de documentos funcionando
- Anamnese publica abrindo por token
- Email/WhatsApp gerando links com URL publica correta
- CORS e CSRF aceitando o frontend hospedado
