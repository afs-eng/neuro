# NeuroAvalia — Contexto do Projeto

## Visão Geral

**NeuroAvalia** é um sistema full-stack para gestão de avaliações neuropsicológicas. Permite ao profissional clínico administrar pacientes, avaliações, anamnese estruturada, aplicação de testes psicológicos padronizados, evolução clínica, documentos e geração de laudos neuropsicológicos.

- **Backend:** Django 5.1+ com Django Ninja (API REST)
- **Frontend:** Next.js 14 (App Router) + React 18 + TypeScript + Tailwind CSS 3 + Radix UI
- **Banco de dados:** SQLite (dev) / PostgreSQL (produção)
- **Gerenciador de pacotes:** `uv` (Python) e `npm` (Node.js)
- **Autenticação:** JWT com refresh tokens, permissões por papel (role)
- **IA assistiva:** Ollama (padrão, modelo `qwen3.5:27b`) ou OpenAI (opcional)

---

## Arquitetura

O backend segue o padrão de **monólito modular orientado a domínio**. Cada app Django em `apps/` é responsável por um domínio de negócio bem definido:

| App | Responsabilidade |
|-----|-----------------|
| `apps/accounts/` | Autenticação, usuários, papéis e permissões |
| `apps/patients/` | Cadastro e dados demográficos do paciente |
| `apps/evaluations/` | Avaliações neuropsicológicas + registros de evolução clínica |
| `apps/anamnesis/` | Templates de anamnese, convites e respostas estruturadas |
| `apps/tests/` | Instrumentos psicológicos — cálculo, normas, classificação (NÚCLEO CLÍNICO) |
| `apps/documents/` | Anexos e documentos vinculados à avaliação |
| `apps/reports/` | Laudos neuropsicológicos estruturados por seções |
| `apps/ai/` | Camada de IA assistiva (isolada do cálculo clínico) |
| `apps/messaging/` | Envio de e-mail (Resend/SMTP) e WhatsApp (Evolution API) |
| `apps/audit/` | Log de auditoria de ações sensíveis |
| `apps/api/` | Roteador principal da API e autenticação |
| `apps/common/` | Utilitários compartilhados |

### Princípios Arquiteturais

1. **Backend é a fonte da verdade** — todo cálculo clínico, classificação normativa e interpretação é feito exclusivamente no backend. O frontend nunca realiza cálculos de escores ou aplicação de normas.
2. **IA é assistiva, não normativa** — o módulo `apps/ai/` é isolado da lógica de cálculo clínico. A IA auxilia na geração textual, mas não calcula, classifica ou emite julgamento clínico.
3. **Separação dos estágios de dados de testes** — cada `TestApplication` armazena separadamente: `raw_payload`, `computed_payload`, `classified_payload` e `reviewed_payload`, garantindo rastreabilidade completa.
4. **Monólito modular preparado para Celery + Redis** — a arquitetura de services permite futura delegação de tarefas assíncronas sem alterar o domínio.

### Fluxo Clínico Principal

```
1. Cadastrar paciente
   → 2. Criar avaliação
   → 3. Coleta de dados (anamneses, documentos, evolução)
   → 4. Aplicar instrumentos psicológicos
   → 5. Backend calcul escores, classifica e persiste
   → 6. Profissional revisa todos os dados
   → 7. Gerar laudo estruturado
```

---

## Instrumentos Psicológicos (`apps/tests/`)

Módulo central de cálculo clínico. Cada instrumento segue o padrão:

```
apps/tests/<instrumento>/
├── config.py          # metadados do instrumento
├── schemas.py         # schemas Pydantic de entrada/saída
├── validators.py      # validação de entrada e limites
├── calculators.py     # lógica de cálculo de escores
├── classifiers.py     # classificação conforme normas
└── interpreters.py    # geração de interpretação textual
```

**Instrumentos suportados:**

| Código | Nome | Faixa Etária |
|--------|------|-------------|
| `wisc4` | WISC-IV | 6–16 anos |
| `bpa2` | BPA-2 | Adulto |
| `ebadep_a` | EBADEP-A | Adulto |
| `ebaped_ij` | EBADEP-IJ | 2–18 anos |
| `epq_j` | EPQ-J | 7–15 anos |
| `etdah_ad` | E-TDAH-AD | Adulto |
| `etdah_pais` | E-TDAH-PAIS | — |
| `fdt` | FDT | 5+ anos |
| `ravlt` | RAVLT | 16+ anos |
| `scared` | SCARED | — |
| `srs2` | SRS-2 | — |

Regras etárias centralizadas em `apps/tests/age_rules.py`.

---

## Estrutura do Projeto

```
neuro/
├── apps/                           # Apps Django por domínio
│   ├── accounts/
│   ├── ai/                         # camadas: providers, guards, prompts, services
│   ├── anamnesis/                  # templates infant/adolescent/adult
│   ├── api/
│   ├── audit/
│   ├── common/
│   ├── documents/
│   ├── evaluations/
│   ├── messaging/
│   ├── patients/
│   ├── reports/                    # builders, services, prompts de laudo
│   └── tests/                      # instrumentos psicológicos
├── config/                         # settings(base/local/production), urls, wsgi, asgi
├── neuro-frontend/                 # Next.js 14
│   ├── app/                        # App Router (dashboard, login, public/anamnesis)
│   ├── components/                 # Componentes React por área
│   ├── services/                   # Consumo da API
│   ├── lib/                        # Utilitários (api.ts)
│   └── types/                      # Tipos TypeScript
├── infra/                          # Artefatos de infraestrutura
├── theme/                          # Tailwind (lado Django)
├── manage.py                       # CLI Django
├── requirements.txt                # Dependências Python
├── pyproject.toml                  # Configuração do projeto Python
├── docker-compose.yml              # Dev completo (Postgres + backend + frontend)
├── docker-compose.prod.yml         # Produção
└── backend.Dockerfile              # Imagem do backend
```

---

## Entidades Principais

| Modelo | Descrição |
|--------|-----------|
| `Patient` | Dados do paciente |
| `Evaluation` | Avaliação neuropsicológica vinculada a um paciente |
| `EvaluationProgressEntry` | Registro cronológico de evolução clínica |
| `EvaluationDocument` | Documento/anexo da avaliação |
| `Instrument` | Catálogo de instrumentos disponíveis |
| `TestApplication` | Aplicação concreta de um instrumento em uma avaliação |
| `AnamnesisTemplate` | Template versionado de anamnese (steps + fields em JSON) |
| `AnamnesisInvite` | Convite externo por token (e-mail ou WhatsApp) |
| `AnamnesisResponse` | Resposta estruturada da anamnese |
| `Report` | Laudo estruturado vinculado a uma avaliação |
| `ReportSection` | Seção individual do laudo |

---

## Endpoints da API

A API é servida por Django Ninja sob `/api/`:

| Domínio | Rotas |
|---------|-------|
| Pacientes | `GET/POST /api/patients/`, `GET/PATCH/DELETE /api/patients/{id}` |
| Avaliações | `GET/POST /api/evaluations/`, `GET /api/evaluations/{id}/progress-entries` |
| Documentos | `GET /api/documents/?evaluation_id=<id>`, `POST /api/documents/upload`, `PATCH/DELETE /api/documents/{id}` |
| Anamnese (interna) | `POST /api/anamnesis/responses/`, `GET/PATCH /api/anamnesis/responses/{id}`, `POST /api/anamnesis/responses/{id}/submit` |
| Anamnese (convites) | `POST /api/anamnesis/invites/`, `POST /api/anamnesis/invites/{id}/send-email`, `/send-whatsapp`, `/cancel` |
| Anamnese (pública) | `GET /api/public/anamnesis/{token}`, `POST /api/public/anamnesis/{token}/save-draft`, `/submit` |
| Testes | `GET /api/tests/instruments/`, `GET/POST /api/tests/applications/`, `POST /api/tests/{instrumento}/submit` |
| Laudos | `GET/POST /api/reports/`, `POST /api/reports/{id}/build`, `GET/PATCH /api/reports/sections/{id}` |

---

## Stack Completa

### Backend
| Tecnologia | Versão |
|------------|--------|
| Python | >= 3.12 |
| Django | >= 5.1, < 5.3 |
| Django Ninja | >= 1.3.0 |
| Pydantic | >= 2.10.0 |
| psycopg | >= 3.2.3 |
| Gunicorn | >= 23.0.0 |
| python-docx | >= 1.2.0 |
| matplotlib | >= 3.10.0 |
| Resend | >= 2.0.0 |

### Frontend
| Tecnologia | Versão |
|------------|--------|
| Next.js | 14.1.0 |
| React | 18.2+ |
| TypeScript | 5.3+ |
| Tailwind CSS | 3.4+ |
| React Query | 5.17+ |
| NextAuth | 4.24+ |
| Radix UI | — |

---

## Comandos Úteis

### Backend (desenvolvimento)

```bash
# Instalar dependências
uv pip install -r requirements.txt

# Executar migrações
uv run python manage.py migrate

# Criar superusuário
uv run python manage.py createsuperuser

# Criar instrumentos de teste
uv run python manage.py create_instruments

# Servidor de desenvolvimento
uv run python manage.py runserver

# Verificar integridade
uv run python manage.py check

# Rodar testes
uv run python manage.py test

# Verificar migrações pendentes
uv run python manage.py makemigrations --check
```

### Frontend (desenvolvimento)

```bash
cd neuro-frontend
npm install          # instalar dependências
npm run dev          # servidor de desenvolvimento (porta 3000)
npm run build        # build de produção
npm run lint         # linting
npm run start        # servidor de produção
```

### Docker Compose (stack completa)

```bash
docker-compose up --build
```

Sobe 3 serviços:
- **PostgreSQL** (porta 5432)
- **Backend Django** (porta 8000)
- **Frontend Next.js** (porta 3000)

O backend acessa o Ollama no host via `host.docker.internal:11434`.

---

## Variáveis de Ambiente

Copie `.env.example` para `.env` e configure:

```env
# Banco (para dev local com SQLite, não precisa)
DATABASE_URL=postgresql://neuro_user:neuro_pass@db:5432/neuro_db

# Django
DJANGO_ENV=local
DEBUG=True
SECRET_KEY=<chave-secreta>

# IA (padrão: Ollama)
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3.5:27b

# E-mail (Resend ou SMTP fallback)
RESEND_API_KEY=re_xxx
RESEND_FROM_EMAIL=NeuroAvalia <noreply@meudominio.com.br>

# WhatsApp (Evolution API — opcional)
EVOLUTION_API_URL=
EVOLUTION_API_KEY=
EVOLUTION_INSTANCE=
```

---

## Deploy

| Serviço | Plataforma |
|---------|-----------|
| Frontend | Vercel (diretório `neuro-frontend/`) |
| Backend | Render Web Service |
| Banco | Render PostgreSQL |

**Backend (Render):**
- Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- Pre-deploy: `python manage.py migrate`
- Start: `gunicorn config.wsgi:application --log-file -`
- Health check: `/healthz/`

Detalhes completos em `DEPLOY.md`.

---

## Documentação de Referência

| Arquivo | Conteúdo |
|---------|----------|
| `README.md` | Visão técnica completa, módulos, endpoints, fluxo do sistema |
| `PROJECT_ARCHITECTURE.md` | Arquitetura de alto nível, organização de apps, fluxo de dados |
| `SKILLS.md` | Stack oficial, princípios, padrões de desenvolvimento |
| `SKILLS_REGRAS_NEGOCIO.md` | Regras de negócio detalhadas |
| `SKILLS_SEGURANCA.md` | Diretrizes de segurança |
| `SKILLS_IA.md` | Diretrizes da camada de IA |
| `DEPLOY.md` | Deploy para Render + Vercel |
| `DOCKER_INSTRUCTIONS.md` | Instruções Docker |
| `FRONTEND_STRUCTURE.md` | Estrutura do frontend Next.js |
---

## Convenções de Desenvolvimento

### Backend
- Lógica de negócio em `services.py` (ou `services/`)
- Consultas ao banco em `selectors.py`
- Endpoints da API são wrappers finos sobre services
- Validação de entrada via schemas Pydantic (Django Ninja)
- Models contêm apenas definição de campos e métodos de instância

### Frontend
- **Zero lógica clínica** no frontend — escores, normas e classificações são sempre calculados no backend
- Toda comunicação com API centralizada em `lib/api.ts`
- Tokens JWT armazenados em `localStorage`
- React Query para data fetching com cache automático

### Geral
- Validação de entrada em todas as APIs
- Sanitização de saída para prevenção de XSS
- Auditoria de todas as ações sensíveis
- IA nunca calcula escores ou aplica normas
