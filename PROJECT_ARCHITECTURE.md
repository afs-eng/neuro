# NeuroAvalia - Arquitetura Full-Stack

## Visão Geral

Projeto de gestão de avaliações neuropsicológicas com backend Django e frontend Next.js, estruturado como monólito modular orientado a domínio.

## Arquitetura de Alto Nível

```
neuro/                              # Projeto Django (Backend)
├── apps/                           # Aplicações por domínio
│   ├── accounts/                   # Usuários e autenticação
│   ├── ai/                        # Camada de IA (LangChain)
│   │   ├── api/
│   │   ├── services/
│   │   ├── providers/
│   │   ├── chains/
│   │   ├── prompts/
│   │   ├── guards/
│   │   ├── logging/
│   │   └── schemas/
│   ├── anamnesis/                  # Questionários de anamnese
│   ├── api/                        # API principal (Ninja)
│   ├── audit/                     # Auditoria de ações
│   │   ├── models.py              # AuditLog
│   │   └── services.py            # AuditService
│   ├── common/                    # Componentes compartilhados
│   ├── documents/                 # Gestão de documentos
│   ├── evaluations/               # Avaliações neuropsicológicas
│   ├── messaging/                 # Sistema de mensagens
│   ├── patients/                  # Gestão de pacientes
│   ├── reports/                   # Laudos e relatórios
│   └── tests/                     # Testes psicológicos (NÚCLEO CLÍNICO)
│       ├── base/
│       │   ├── types.py           # Tipos (TestContext, ComputedScore, etc)
│       │   ├── interfaces.py      # Protocolos (ICalculator, IClassifier)
│       │   └── exceptions.py      # Exceções customizadas
│       ├── models/
│       │   ├── instruments.py     # Instrument
│       │   ├── applications.py    # TestApplication
│       │   └── templates.py       # InterpretationTemplate
│       ├── services/
│       │   ├── application_service.py
│       │   ├── scoring_service.py
│       │   └── interpretation_service.py
│       ├── selectors.py           # Queries do domínio
│       ├── registry.py            # Registro de instrumentos
│       ├── api/
│       │   ├── router.py
│       │   ├── endpoints.py
│       │   └── schemas.py
│       ├── norms/                 # Tabelas normativas
│       └── instrumentos/
│           ├── wisc4/             # WISC-IV
│           ├── bpa2/              # BPA-2
│           ├── ebadep_a/          # EBADEP-A
│           ├── ebaped_ij/         # EBAPED-IJ
│           ├── epq_j/            # EPQ-J
│       ├── etdah_ad/          # ETDAH-AD
│       ├── etdah_pais/        # ETDAH-PAIS
│       ├── fdt/               # FDT
│       ├── ravlt/             # RAVLT
│       └── scared/            # SCARED

│
├── config/                        # Configurações Django
│   ├── settings/
│   │   ├── base.py               # Configurações base
│   │   ├── local.py              # Desenvolvimento
│   │   └── production.py          # Produção
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── theme/                         # Tema Tailwind
│   └── static_src/
│
├── infra/                         # Infraestrutura Docker
│
└── manage.py


neuro-frontend/                   # Projeto Next.js (Frontend)
├── app/
│   ├── dashboard/
│   │   ├── accounts/
│   │   ├── ai/
│   │   ├── documents/
│   │   ├── evaluations/
│   │   ├── patients/
│   │   ├── reports/
│   │   ├── tests/
│   │   └── page.tsx
│   ├── login/
│   ├── layout.tsx
│   └── page.tsx
│
├── components/
│   ├── ui/
│   ├── layout/
│   ├── patients/
│   ├── tests/
│   └── anamnesis/
│
├── lib/
│   ├── api.ts
│   └── utils.ts
│
├── services/
├── types/
│
└── package.json
```

## Padrão Interno dos Apps

Cada app segue uma estrutura modular:

```
apps/<app_name>/
├── models/           # Modelos Django
├── api/              # Endpoints Ninja
├── services/         # Lógica de negócio
├── selectors.py      # Consultas DB
├── validators.py     # Validações
├── permissions.py    # Permissões
├── workflows.py      # Fluxos complexos
├── storage/          # Integração com storage
└── apps.py
```

## Camada de IA (`apps/ai/`)

Regras obrigatórias:
- LangChain existe apenas aqui
- IA é apenas **assistiva**
- IA **não calcula** escore, percentil, classificação ou norma
- IA **não substitui** revisão humana
- IA recebe dados **já estruturados** pelo backend
- IA não acessa banco diretamente

```
apps/ai/
├── api/              # Endpoints para IA
├── services/         # AIService
├── providers/        # OpenAI, Anthropic, etc
├── chains/          # LangChain chains
├── prompts/          # Templates de prompt
├── guards/          # Validations (AIGuard)
├── logging/         # AILogger
└── schemas/         # Schemas Pydantic
```

## Módulo `tests` (Núcleo Clínico)

Estrutura padrão de cada instrumento:

```
apps/tests/<instrumento>/
├── __init__.py      # Registra instrumento
├── config.py        # Configuração do instrumento
├── schemas.py       # Schemas de input/output
├── validators.py    # Validações específicas
├── loaders.py       # Carregamento de tabelas
├── calculators.py  # Cálculo de escores
├── classifiers.py  # Classificações clínicas
├── interpreters.py  # Interpretações
└── constants.py    # Constantes
```

### Separação de Dados

Toda aplicação de teste segue esta estrutura:

| Campo | Descrição |
|-------|-----------|
| `raw_payload` | Dado bruto digitado |
| `computed_payload` | Resultado calculado (escore, percentil) |
| `classified_payload` | Classificação clínica |
| `interpretation_text` | Interpretação |

## Camada de Auditoria (`apps/audit/`)

Modelo AuditLog para rastrear ações críticas:
- CRUD de pacientes, avaliações, laudos
- Exportação e impressão
- Login/logout
- Acesso a dados sensíveis

## Fluxo de Dados

```
Usuário (Frontend Next.js)
    │
    ▼ HTTP JSON
┌─────────────────────────────┐
│    Django Ninja API         │
│  (apps/api, apps/tests)     │
└──────────────┬──────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────────┐    ┌───────▼─────┐
│  Services  │    │     AI      │
│ (negocio)  │    │ (assistivo) │
└─────┬──────┘    └─────────────┘
      │
┌─────▼──────┐
│ Django ORM │
│ + PostgreSQL│
└────────────┘
```

## Endpoints API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/patients/` | Lista pacientes |
| POST | `/api/patients/` | Cria paciente |
| GET | `/api/patients/{id}/` | Detalhes |
| PUT | `/api/patients/{id}/` | Atualiza |
| DELETE | `/api/patients/{id}/` | Remove |
| GET | `/api/evaluations/` | Lista avaliações |
| POST | `/api/evaluations/` | Cria avaliação |
| GET | `/api/tests/wisc4/` | Info WISC-IV |
| POST | `/api/tests/wisc4/calculate/` | Calcula WISC-IV |
| GET | `/api/tests/{code}/result/{id}/` | Resultado |
| GET | `/api/ai/generate/` | Geração IA |
| GET | `/api/audit/logs/` | Logs de auditoria |
| POST | `/api/auth/login/` | Login JWT |

## Testes Psicológicos

| Código | Nome | Faixa Etária |
|--------|------|--------------|
| wisc4 | WISC-IV | 6-16 anos |
| bpa2 | BPA-2 | Adulto |
| ebadep_a | EBADEP-A | Adulto |
| ebaped_ij | EBAPED-IJ | Infantojuvenil |
| epq_j | EPQ-J | 7-15 anos |
| etdah_ad | ETDAH-AD | 12+ anos |
| etdah_pais | ETDAH-PAIS | 2-17 anos |
| fdt | FDT | 5+ anos |
| ravlt | RAVLT | 16+ anos |
| scared | SCARED | 9-18 anos (Autorrelato) / Crianças e Adol. (Pais) |


## Tecnologias

| Camada | Tecnologia |
|--------|------------|
| Backend | Django 4+ |
| API | Django Ninja |
| Frontend | Next.js 14 (App Router) |
| UI | Tailwind CSS |
| Auth | JWT |
| Database | SQLite (dev) / PostgreSQL (prod) |
| IA | LangChain (backend) |
| Message Queue | Pronto para Celery + Redis |
| Deploy | Docker, Vercel + Railway/Render |

## Estrutura de Diretórios

```
/home/andre/neuro/
├── apps/              # 12 apps Django
├── config/           # Settings separados
├── theme/            # Tailwind
├── neuro-frontend/   # Next.js
├── staticfiles/
├── infra/            # Docker
├── docker-compose.yml
├── docker-compose.prod.yml
├── pyproject.toml
├── requirements.txt
└── uv.lock
```

## Pronto para Crescer

A arquitetura está preparada para:
- Celery + Redis (tarefas assíncronas)
- Nginx (reverse proxy)
- Workers separados (processamento intenso)
- Cache distribuído
- Escalabilidade horizontal
