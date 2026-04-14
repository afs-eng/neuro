# 🚀 Deploy em Produção — NeuroAvalia

## Checklist de Deploy

### 1. Backend no Render

#### 1.1 Criar Banco PostgreSQL no Render
1. Acesse https://render.com/dashboard
2. **New → PostgreSQL**
3. Preencha:
   - **Name**: `neuro-db`
   - **Database**: `neuro_db`
   - **User**: `neuro_user`
4. Copie a **Internal Database URL** (parece com `postgresql://neuro_user:xxx@db-xxxx-a.ondigitalocean.com:25060/neuro_db?sslmode=require`)

#### 1.2 Criar Web Service (Backend)
1. **New → Web Service**
2. Conecte o repositório GitHub: `seu-usuario/neuro` (ou o nome correto)
3. Configure:
   - **Root Directory**: `.` (raiz)
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
   - **Pre-Deploy Command**:
     ```bash
     python manage.py migrate
     ```
   - **Start Command**:
     ```bash
     gunicorn config.wsgi:application --log-file -
     ```
   - **Health Check Path**: `/healthz/`
   - **Plan**: Free (teste) ou Starter (produção)

#### 1.3 Variáveis de Ambiente do Backend
No painel do Web Service → **Environment**, adicione:

| Variável | Valor | Exemplo |
|----------|-------|---------|
| `DJANGO_ENV` | `production` | `production` |
| `DEBUG` | `False` | `False` |
| `SECRET_KEY` | Gere uma nova | `openssl rand -hex 64` |
| `DATABASE_URL` | URL do PostgreSQL (item 1.1) | `postgresql://neuro_user:xxx@...` |
| `DATABASE_SSL_REQUIRE` | `True` | `True` |
| `ALLOWED_HOSTS` | Domínio do Render | `neuro-k06p.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | Render + Vercel | `https://neuro-k06p.onrender.com,https://neuro-app.vercel.app` |
| `CORS_ALLOWED_ORIGINS` | Vercel | `https://neuro-app.vercel.app` |
| `FRONTEND_BASE_URL` | URL do Vercel | `https://neuro-app.vercel.app` |
| `BACKEND_PUBLIC_URL` | URL do Render | `https://neuro-k06p.onrender.com` |
| `ALLOW_VERCEL_PREVIEWS` | `True` | `True` |
| `RESEND_API_KEY` | Chave Resend (opcional) | `re_xxx` |
| `RESEND_FROM_EMAIL` | Email remetente | `NeuroAvalia <noreply@meudominio.com.br>` |

> **Nota**: O backend já suporta automaticamente domínios Vercel via regex (`ALLOW_VERCEL_PREVIEWS=True`).

#### 1.4 Executar comandos pós-deploy
Após o primeiro deploy bem-sucedido, acesse o **Shell** no painel do Render e execute:

```bash
python manage.py createsuperuser
python manage.py create_instruments
```

#### 1.5 Verificar Health
Acesse: `https://seu-dominio-render.onrender.com/healthz/`
Deve retornar: `{"status": "ok"}`

---

### 2. Frontend no Vercel

#### 2.1 Configurar Projeto
1. Acesse https://vercel.com
2. **New Project**
3. Importe o repositório GitHub
4. Configure:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `neuro-frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`

#### 2.2 Variáveis de Ambiente do Frontend
No painel do Vercel → **Settings → Environment Variables**, adicione:

| Variável | Valor | Exemplo |
|----------|-------|---------|
| `NEXT_PUBLIC_API_BASE_URL` | URL do Render | `https://neuro-k06p.onrender.com` |
| `INTERNAL_API_BASE_URL` | URL do Render | `https://neuro-k06p.onrender.com` |
| `NEXT_PUBLIC_APP_URL` | URL do Vercel | `https://neuro-app.vercel.app` |

> **Importante**: Não adicione `/api` no final das URLs.

#### 2.3 Deploy
1. Clique em **Deploy**
2. Aguarde o build (~2 min)
3. Acesse a URL gerada: `https://neuro-app.vercel.app`

---

### 3. Testes de Validação

#### 3.1 Login
1. Acesse `https://seu-frontend.vercel.app/login`
2. Faça login com o superusuário criado no item 1.4
3. Verifique se o dashboard carrega corretamente

#### 3.2 Criar Avaliação Completa
1. Cadastre um paciente
2. Crie uma avaliação
3. Envie um convite de anamnese (e-mail ou gere o link manualmente)
4. **Teste o link**: abra em aba anônima
5. Preencha e envie a anamnese

#### 3.3 Verificar Link de Anamnese
O link deve ter o formato:
```
https://seu-frontend.vercel.app/public/anamnesis/{token}
```

E **NÃO**:
```
https://seu-frontend.vercel.app/public/anamnesis/{token}?vercelToolbar=...
```

---

### 4. Troubleshooting

#### Problema: "Convite inválido" na anamnese
**Causa**: Frontend não consegue acessar o backend.
**Solução**:
- Verifique se `NEXT_PUBLIC_API_BASE_URL` está correto no Vercel
- Verifique se o backend está rodando (`/healthz/` responde)

#### Problema: Erro de CORS
**Causa**: Origem do frontend não está permitida no backend.
**Solução**:
- Adicione a URL do Vercel em `CSRF_TRUSTED_ORIGINS` e `CORS_ALLOWED_ORIGINS` no Render
- Verifique se `ALLOW_VERCEL_PREVIEWS=True`

#### Problema: Erro 403 CSRF
**Causa**: Cookie CSRF não está sendo enviado corretamente.
**Solução**:
- Verifique se `CSRF_TRUSTED_ORIGINS` inclui a URL do Vercel
- Verifique se `SESSION_COOKIE_SECURE=True` e `CSRF_COOKIE_SECURE=True`

#### Problema: Link da anamnese gera conta no Vercel
**Causa**: A rota `/public/anamnesis/[token]` não foi reconhecida pelo Next.js.
**Solução**:
- Verifique se `neuro-frontend/app/public/anamnesis/[token]/page.tsx` existe
- Faça um redeploy no Vercel após confirmar que o arquivo está no repositório
- Verifique os logs de build no Vercel

---

### 5. URLs de Referência

| Serviço | URL Base | Exemplo |
|---------|----------|---------|
| Backend (Render) | `https://neuro-k06p.onrender.com` | `https://neuro-k06p.onrender.com/api/patients/` |
| Frontend (Vercel) | `https://neuro-app.vercel.app` | `https://neuro-app.vercel.app/public/anamnesis/{token}` |

---

### 6. Comandos Úteis

```bash
# Gerar SECRET_KEY
openssl rand -hex 64

# Verificar integridade do backend localmente
python manage.py check --deploy

# Verificar migrações pendentes
python manage.py makemigrations --check

# Rodar build do frontend localmente
cd neuro-frontend && npm run build
```

---

### 7. Pós-Deploy

- [ ] Backup automático do PostgreSQL configurado
- [ ] Monitoramento de logs no Render ativado
- [ ] Domínio customizado configurado (opcional)
- [ ] SSL/HTTPS verificado
- [ ] E-mail (Resend) funcionando
- [ ] WhatsApp (Evolution API) configurado (opcional)
- [ ] IA (Ollama/OpenAI) configurada (opcional)
