# NeuroAvalia - README Tecnico

## Visao Geral

NeuroAvalia e um sistema full stack para gestao de pacientes, avaliacoes neuropsicologicas, aplicacao de testes, anamnese estruturada, documentos, evolucao clinica e laudos.

- Backend: Django
- API: Django Ninja
- Frontend: Next.js 14 (App Router)
- Banco atual: SQLite
- Dominio principal: pacientes, avaliacoes, anamnese, instrumentos psicologicos e relatorios clinicos

---

## Stack Principal

### Backend

- Python
- Django
- Django Ninja
- ORM nativo do Django
- Migrations Django
- Envio de e-mail desacoplado por service layer

### Frontend

- Next.js 14
- React
- TypeScript
- Tailwind CSS
- Componentes reutilizaveis no dashboard e em formularios publicos

---

## Estrutura de Pastas

```text
neuro/
├── apps/
│   ├── accounts/          # autenticacao, usuarios e permissoes
│   ├── anamnesis/         # templates, convites e respostas de anamnese
│   ├── api/               # auth e roteamento global da API
│   ├── common/            # utilitarios compartilhados
│   ├── documents/         # documentos vinculados a avaliacao
│   ├── evaluations/       # avaliacoes e evolucao clinica
│   ├── messaging/         # envio por email e WhatsApp
│   ├── patients/          # cadastro e gestao de pacientes
│   ├── reports/           # laudos estruturados
│   └── tests/             # instrumentos e aplicacoes de testes
├── config/
│   ├── settings/
│   ├── templates/
│   ├── static/
│   ├── staticfiles/
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── db.sqlite3
├── neuro-frontend/
│   ├── app/
│   ├── components/
│   │   └── anamnesis/
│   └── lib/
├── theme/
├── PROJECT_ARCHITECTURE.md
└── manage.py
```

---

## Modulos do Backend

### `apps/accounts/`

Responsavel por autenticacao, usuarios, papeis e permissoes.

### `apps/patients/`

Responsavel pelo cadastro do paciente e seus dados demograficos.

Entidade central:

- `Patient`

### `apps/evaluations/`

Representa a avaliacao neuropsicologica vinculada a um paciente.

Entidades principais:

- `Evaluation`
- `EvaluationProgressEntry`

Responsabilidades:

- criar avaliacao
- vincular paciente
- servir como contexto dos testes
- registrar evolucao clinica cronologica

### `apps/documents/`

Responsavel por anexos da avaliacao.

Entidade principal:

- `EvaluationDocument`

Responsabilidades:

- upload de arquivos
- serializacao e listagem por avaliacao
- marcacao de relevancia para o laudo

### `apps/anamnesis/`

Dominio proprio da anamnese estruturada.

Entidades principais:

- `AnamnesisTemplate`
- `AnamnesisInvite`
- `AnamnesisResponse`

Responsabilidades:

- manter templates versionados de anamnese
- permitir preenchimento interno no dashboard
- permitir preenchimento externo por link seguro com token
- suportar rascunho, envio final e revisao
- armazenar respostas em JSON estruturado para uso clinico e futuro laudo

Estrutura resumida:

```text
apps/anamnesis/
├── api/
│   ├── endpoints.py
│   ├── router.py
│   └── schemas.py
├── migrations/
├── templates/
│   ├── infant.py
│   ├── adolescent.py
│   └── adult.py
├── constants.py
├── models.py
├── selectors.py
└── services.py
```

### `apps/messaging/`

Camada desacoplada de mensageria.

Arquivos principais:

- `email_service.py`
- `whatsapp_service.py`
- `services.py`

Responsabilidades:

- envio de convite de anamnese por e-mail
- geracao de link de WhatsApp com mensagem pronta
- permitir futura troca por integracao oficial sem alterar o dominio clinico

### `apps/reports/`

Modulo de laudo estruturado por secoes.

Entidades principais:

- `Report`
- `ReportSection`

Arquivos principais:

- `builders.py`
- `models.py`
- `selectors.py`
- `services.py`

Responsabilidades:

- snapshot estruturado da avaliacao
- secoes geradas e editaveis
- consolidacao futura de anamnese, testes, evolucao e documentos

### `apps/tests/`

Nucleo funcional dos instrumentos.

Estrutura resumida:

```text
apps/tests/
├── api/
├── age_rules.py          # regras etarias centralizadas dos instrumentos
├── base/
├── models/
├── services/
├── registry.py
├── selectors.py
├── urls.py
├── views.py
├── management/commands/
│   └── create_instruments.py
├── wisc4/
├── bpa2/
├── ebadep_a/
├── ebaped_ij/
├── epq_j/
├── etdah_ad/
└── fdt/
```

Observacao importante:

- `EBADEP-IJ` continua usando a pasta `apps/tests/ebaped_ij/`, mas as rotas e o codigo funcional usam `ebadep_ij`

---

## Padrao de Implementacao de Testes

Cada instrumento segue, em geral, a mesma organizacao:

```text
apps/tests/<instrumento>/
├── __init__.py
├── config.py
├── schemas.py
├── validators.py
├── calculators.py
├── interpreters.py
└── classifiers.py
```

Fluxo interno:

1. recebe dados brutos
2. valida formato e limites
3. calcula escores
4. classifica segundo normas
5. gera interpretacao textual
6. persiste em `TestApplication`

---

## Instrumentos Ja Integrados

- `wisc4`
- `bpa2`
- `ebadep_a`
- `ebadep_ij`
- `epq_j`
- `etdah_ad`
- `fdt`

As regras etarias dos instrumentos agora ficam centralizadas em `apps/tests/age_rules.py` e sao expostas pela API de instrumentos para o frontend.

---

## Modelos Centrais

### `Patient`

Paciente do sistema.

### `Evaluation`

Avaliacao associada a um paciente.

### `EvaluationProgressEntry`

Registro cronologico do processo clinico da avaliacao.

### `EvaluationDocument`

Documento anexado a uma avaliacao.

### `Instrument`

Cadastro do teste disponivel no sistema.

Campos importantes:

- `code`
- `name`
- `category`
- `version`
- `is_active`

### `TestApplication`

Aplicacao concreta de um instrumento em uma avaliacao.

Campos importantes:

- `evaluation`
- `instrument`
- `applied_on`
- `raw_payload`
- `computed_payload`
- `classified_payload`
- `reviewed_payload`
- `interpretation_text`
- `is_validated`

### `AnamnesisTemplate`

Template versionado de anamnese estruturada.

Campos importantes:

- `code`
- `name`
- `target_type`
- `version`
- `schema_payload`
- `is_active`

### `AnamnesisInvite`

Convite externo para preenchimento por link seguro.

Campos importantes:

- `evaluation`
- `patient`
- `template`
- `recipient_name`
- `recipient_email`
- `recipient_phone`
- `channel`
- `token`
- `status`
- `sent_at`
- `opened_at`
- `completed_at`
- `expires_at`

### `AnamnesisResponse`

Resposta estruturada da anamnese.

Campos importantes:

- `invite` (opcional)
- `evaluation`
- `patient`
- `template`
- `response_type`
- `source`
- `status`
- `answers_payload`
- `summary_payload`
- `submitted_by_name`
- `submitted_by_relation`
- `reviewed_by`

### `Report`

Laudo estruturado vinculado a uma avaliacao.

### `ReportSection`

Secao editavel e gerada do laudo.

---

## API Backend

O backend usa Django Ninja.

Rotas principais:

- `/api/accounts/...`
- `/api/patients/...`
- `/api/evaluations/...`
- `/api/documents/...`
- `/api/anamnesis/...`
- `/api/public/anamnesis/...`
- `/api/tests/...`
- `/api/reports/...`

### Endpoints relevantes por dominio

#### Pacientes

- `/api/patients/`
- `/api/patients/{id}`

#### Avaliacoes

- `/api/evaluations/`
- `/api/evaluations/{id}`
- `/api/evaluations/{id}/progress-entries`

#### Documentos

- `GET /api/documents/?evaluation_id=<id>`
- `POST /api/documents/upload`
- `PATCH /api/documents/{id}`
- `DELETE /api/documents/{id}`

#### Anamnese

Templates:

- `GET /api/anamnesis/templates/`
- `GET /api/anamnesis/templates/{id}`

Respostas internas:

- `POST /api/anamnesis/responses/`
- `GET /api/anamnesis/responses/?evaluation_id=<id>`
- `GET /api/anamnesis/responses/{id}`
- `PATCH /api/anamnesis/responses/{id}`
- `POST /api/anamnesis/responses/{id}/submit`
- `PATCH /api/anamnesis/responses/{id}/review`

Convites externos:

- `POST /api/anamnesis/invites/`
- `GET /api/anamnesis/invites/?evaluation_id=<id>`
- `GET /api/anamnesis/invites/{id}`
- `POST /api/anamnesis/invites/{id}/send-email`
- `POST /api/anamnesis/invites/{id}/send-whatsapp`
- `POST /api/anamnesis/invites/{id}/resend`
- `POST /api/anamnesis/invites/{id}/cancel`

Publicos por token:

- `GET /api/public/anamnesis/{token}`
- `POST /api/public/anamnesis/{token}/save-draft`
- `POST /api/public/anamnesis/{token}/submit`

#### Testes

- `/api/tests/instruments/`
- `/api/tests/applications/`
- `/api/tests/<instrumento>/submit`
- `/api/tests/<instrumento>/result/<application_id>`

#### Laudos

- `/api/reports/`
- `/api/reports/{id}`
- `/api/reports/{id}/build`
- `/api/reports/sections/{id}`

---

## Frontend Next.js

O frontend usa App Router e organiza o dashboard por dominio.

Estrutura resumida:

```text
neuro-frontend/app/
├── layout.tsx
├── page.tsx
├── login/
├── public/
│   └── anamnesis/
│       └── [token]/page.tsx
└── dashboard/
    ├── layout.tsx
    ├── page.tsx
    ├── accounts/
    ├── ai/
    ├── documents/
    ├── reports/
    ├── patients/
    ├── evaluations/
    │   ├── page.tsx
    │   ├── new/page.tsx
    │   └── [id]/
    │       ├── page.tsx
    │       └── anamnesis/
    │           ├── page.tsx
    │           ├── new/page.tsx
    │           └── [anamnesisId]/page.tsx
    └── tests/
```

### Componentes reutilizaveis de anamnese

```text
neuro-frontend/components/anamnesis/
├── FieldRenderer.tsx
├── FormStepRenderer.tsx
├── InternalAnamnesisEditor.tsx
├── ProgressHeader.tsx
├── RepeaterField.tsx
├── ReviewSummary.tsx
└── types.ts
```

### Padrao de testes no frontend

```text
neuro-frontend/app/dashboard/tests/<instrumento>/
├── page.tsx
└── [id]/result/page.tsx
```

---

## Fluxo Principal do Sistema

### 1. Cadastro do paciente

Usuario cria ou edita paciente.

### 2. Criacao da avaliacao

Avaliacao e vinculada ao paciente.

### 3. Coleta de dados clinicos

Na avaliacao, o sistema passa a suportar:

- anamnese interna estruturada
- convite externo de anamnese por token
- upload de documentos
- evolucao clinica

### 4. Aplicacao de testes

Frontend abre formulario do instrumento e submete para a API.

### 5. Correcao e persistencia

Backend calcula, classifica e persiste resultado em `TestApplication`.

### 6. Revisao clinica

Profissional revisa:

- anamnese
- testes
- evolucao
- documentos

### 7. Laudo

Laudo estruturado consome snapshot da avaliacao sem recalcular testes.

---

## Persistencia e Fonte da Verdade

### Testes

- `raw_payload`
- `computed_payload`
- `classified_payload`
- `reviewed_payload`

### Anamnese

- `answers_payload`
- `summary_payload`
- `status`
- `source`

### Laudo

- `snapshot_payload`
- `generated_text`
- `edited_text`
- `final_text`

O backend continua sendo a fonte da verdade para:

- regras de negocio
- normas e idade dos testes
- estados de convite/resposta
- snapshot estrutural do laudo

---

## Anamnese Estruturada

O sistema agora possui uma base unica de formulario configuravel, compartilhada entre preenchimento interno e externo.

Cada template possui:

- `title`
- `description`
- `steps`

Cada step possui:

- `id`
- `title`
- `description`
- `fields`

Cada field pode ter:

- `id`
- `label`
- `type`
- `required`
- `placeholder`
- `help_text`
- `options`
- `conditional`
- `item_fields` para `repeater`

Tipos suportados atualmente:

- `text`
- `textarea`
- `number`
- `date`
- `select`
- `radio`
- `checkbox`
- `multiselect`
- `phone`
- `email`
- `repeater`
- `yes_no`

Modelos implementados:

- anamnese infantil
- anamnese adolescente
- anamnese adulta

---

## Laudo Estruturado

O modulo `reports` ja foi preparado para consumir dados estruturados.

Atualmente o snapshot do laudo inclui:

- dados da avaliacao
- dados do paciente
- documentos
- evolucao
- testes validados

Base preparada para proxima integracao:

- respostas estruturadas de anamnese

Arquivo chave:

- `apps/reports/builders.py`

---

## Comandos Uteis

### Backend

```bash
uv run python manage.py check
uv run python manage.py migrate
uv run python manage.py makemigrations --check
uv run python manage.py create_instruments
uv run python manage.py test
```

### Frontend

```bash
npm run lint
npm run build
```

---

## Estado Atual do Projeto

Ja implementado:

- pacientes
- avaliacoes
- testes com resultados
- regras etarias centralizadas dos instrumentos
- documentos vinculados a avaliacao
- evolucao clinica
- laudo estruturado por secoes
- anamnese interna e externa por token
- envio por email e WhatsApp via camada de mensageria

Preparado para expansao:

- integracao completa da anamnese no snapshot do laudo
- resumos clinicos automáticos em `summary_payload`
- integracao oficial futura de WhatsApp

---

## Resumo Rapido Para Outra IA

> NeuroAvalia e um sistema full stack de avaliacao neuropsicologica com Django + Django Ninja no backend e Next.js 14 no frontend. O dominio central envolve pacientes, avaliacoes, anamnese estruturada, documentos, evolucao clinica, testes psicologicos e laudos. Cada teste vive em um modulo proprio em `apps/tests/<instrumento>/`. A anamnese vive em `apps/anamnesis/` com templates configuraveis por `steps` e `fields`, convites externos por token e respostas internas/externas persistidas em JSON. O laudo estruturado em `apps/reports/` consome snapshot de avaliacao, documentos, evolucao e testes, e esta preparado para incorporar a anamnese nas proximas iteracoes.
