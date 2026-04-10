# Project Architecture

## Visao Geral

O repositorio contem uma arquitetura full-stack com duas frentes principais:

- backend Django modular em `apps/`
- frontend Next.js em `neuro-frontend/`

O estado atual e de transicao controlada: o sistema novo em Next.js ja cobre o dashboard principal, enquanto o backend Django ainda mantem telas server-rendered em `config/templates/` para partes legadas e apoio operacional.

## Estrutura de Alto Nivel

```text
neuro/
├── apps/                      # dominios Django
│   ├── accounts/
│   ├── ai/
│   ├── anamnesis/
│   ├── api/
│   ├── audit/
│   ├── common/
│   ├── documents/
│   ├── evaluations/
│   ├── messaging/
│   ├── patients/
│   ├── reports/
│   └── tests/
├── config/                    # settings, urls, templates e assets Django
├── infra/                     # artefatos de infraestrutura
├── theme/                     # integracao Tailwind do lado Django
├── neuro-frontend/            # frontend Next.js
├── files/
├── media/
├── static/
├── staticfiles/
├── manage.py
├── pyproject.toml
├── docker-compose.yml
└── docker-compose.prod.yml
```

## Backend Django

### Organizacao por dominio

Cada app do backend concentra responsabilidade de negocio bem definida.

- `apps/accounts/`: autenticacao, usuarios e regras de acesso
- `apps/ai/`: camada assistiva de IA, isolada do calculo clinico
- `apps/anamnesis/`: templates, convites e respostas de anamnese
- `apps/api/`: roteador principal da API, auth e endpoints transversais
- `apps/audit/`: rastreabilidade de eventos sensiveis
- `apps/common/`: utilitarios compartilhados
- `apps/documents/`: anexos por avaliacao
- `apps/evaluations/`: avaliacao clinica e progresso
- `apps/messaging/`: email e WhatsApp desacoplados
- `apps/patients/`: cadastro e dados demograficos
- `apps/reports/`: geracao e organizacao de laudos
- `apps/tests/`: motor dos instrumentos psicologicos

### Estrutura recorrente dos apps

Nem todos os apps seguem exatamente a mesma arvore, mas o padrao dominante hoje e:

```text
apps/<dominio>/
├── api/
├── migrations/
├── models.py
├── selectors.py
├── services.py        # ou services/
├── views.py           # quando ha tela Django
├── urls.py            # quando ha rotas Django
└── apps.py
```

## API e Interfaces

O backend expoe duas interfaces principais:

### 1. API JSON

- definida principalmente por `apps/api/router.py`
- publicada em `config/urls.py` sob `/api/`
- consumida pelo frontend Next.js

### 2. Telas Django server-rendered

Ainda existem rotas HTML no backend, por exemplo:

- `/` para dashboard legado
- `/pacientes/`
- `/avaliacoes/`
- `/testes/`
- `/relatorios/`

Isso mostra que a arquitetura atual e hibrida, nao exclusivamente SPA ou API-only.

## Frontend Next.js

O frontend novo fica em `neuro-frontend/` e usa App Router.

### Camadas principais

- `app/`: rotas, layouts e paginas
- `components/`: componentes de interface por area
- `services/`: consumo da API Django
- `lib/`: infraestrutura compartilhada, incluindo `api.ts`
- `types/`: contratos TypeScript

### Areas funcionais expostas

- autenticacao: `login`, `register`, `forgot-password`, `reset-password`
- dashboard autenticado
- pacientes
- avaliacoes
- documentos
- laudos
- testes psicologicos
- anamnese publica por token

## Dominio Clinico Central

O fluxo principal do sistema gira em torno destas entidades:

1. `Patient`
2. `Evaluation`
3. `TestApplication`
4. `AnamnesisResponse`
5. `EvaluationDocument`
6. `Report`

Resumo do fluxo:

1. cadastrar paciente
2. abrir avaliacao
3. registrar anamnese, documentos e progresso
4. aplicar instrumentos
5. calcular e classificar resultados no backend
6. consolidar laudo

## Modulo `apps/tests/`

Esse e o nucleo de calculo dos instrumentos.

Estrutura atual resumida:

```text
apps/tests/
├── api/
├── base/
├── management/
├── migrations/
├── models/
├── norms/
├── permissions/
├── services/
├── validators/
├── registry.py
├── selectors.py
├── age_rules.py
├── models.py
├── urls.py
├── views.py
├── bpa2/
├── ebadep_a/
├── ebaped_ij/
├── epq_j/
├── etdah_ad/
├── etdah_pais/
├── fdt/
├── ravlt/
├── scared/
├── srs2/
└── wisc4/
```

Padrao esperado por instrumento:

```text
apps/tests/<instrumento>/
├── __init__.py
├── config.py
├── schemas.py
├── validators.py
├── calculators.py
├── classifiers.py
└── interpreters.py
```

Responsabilidades do backend de testes:

- validar payload bruto
- aplicar regras etarias
- calcular escores
- classificar segundo normas
- montar payload computado e classificado
- persistir `TestApplication`

Instrumentos atualmente presentes no repositorio:

- `bpa2`
- `ebadep_a`
- `ebaped_ij`
- `epq_j`
- `etdah_ad`
- `etdah_pais`
- `fdt`
- `ravlt`
- `scared`
- `srs2`
- `wisc4`

## Camada de IA

`apps/ai/` permanece isolado do nucleo clinico.

Estrutura atual:

```text
apps/ai/
├── api/
├── chains/
├── guards/
├── logging/
├── prompts/
├── providers/
├── schemas/
└── services/
```

Diretrizes arquiteturais implicitas no codigo e na documentacao do projeto:

- IA e assistiva, nao normativa
- calculo clinico continua no backend de dominio
- acesso a IA passa por guardrails e prompts controlados

## Anamnese

`apps/anamnesis/` contem o fluxo estruturado de formularios clinicos.

Estrutura atual:

```text
apps/anamnesis/
├── api/
├── templates/
├── migrations/
├── constants.py
├── models.py
├── selectors.py
└── services.py
```

No frontend, esse dominio aparece em dois contextos:

- edicao interna por avaliacao
- preenchimento publico por token em `app/public/anamnesis/[token]/page.tsx`

## Relatorios e Documentos

### `apps/documents/`

Responsavel por anexos de avaliacao e metadados associados.

### `apps/reports/`

Concentra geracao e organizacao do laudo. Hoje a estrutura inclui tanto `services.py` quanto uma pasta `services/`, alem de `builders/` e `prompts/`, indicando que o modulo cresceu alem do formato simples de um unico arquivo.

## Mensageria

`apps/messaging/` desacopla o envio de comunicacoes do restante do dominio.

Arquivos principais:

- `email_service.py`
- `whatsapp_service.py`
- `services.py`

Isso facilita troca futura de provedor sem contaminar os fluxos clinicos.

## Configuracao e Deploy

### Config Django

```text
config/
├── settings/
│   ├── base.py
│   ├── local.py
│   └── production.py
├── templates/
├── static/
├── staticfiles/
├── urls.py
├── asgi.py
└── wsgi.py
```

### Artefatos operacionais

- `docker-compose.yml`
- `docker-compose.prod.yml`
- `backend.Dockerfile`
- `render.yaml`
- `VERCEL_DEPLOY.md`
- `DEPLOY.md`

## Fluxo de Dados

```text
Usuario
  |
  | HTTP / JSON
  v
Next.js frontend (`neuro-frontend`)
  |
  | fetch em `lib/api.ts`
  v
Django API (`/api/`)
  |
  +--> services / selectors / models por dominio
  |
  +--> modulo `apps/tests/` para calculo clinico
  |
  +--> modulo `apps/ai/` para apoio assistivo
  v
Banco de dados e arquivos
```

## Stack Atual

- Backend: Django 5.1+
- API: Django Ninja
- Frontend: Next.js 14.1
- UI: React 18 + Tailwind CSS 3 + Radix UI
- Banco: SQLite no ambiente atual, com caminho para PostgreSQL em producao
- Deploy: Render, Vercel e Docker

## Observacoes Importantes

- O repositorio ainda contem uma camada Django HTML legado em paralelo ao frontend Next.js.
- O frontend consome a API diretamente e usa token no `localStorage`.
- `apps/tests/` e o centro do comportamento clinico deterministico.
- `apps/ai/` deve continuar separado da logica normativa e de escore.
- A arquitetura atual privilegia modularidade por dominio, mas sem impor uma rigidez artificial unica para todos os apps.
