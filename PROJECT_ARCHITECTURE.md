# NeuroAvalia - Arquitetura Full-Stack

```
neuro/                              # Projeto Django (Backend)
├── apps/
│   ├── accounts/                   # Usuários e autenticação
│   │   ├── api/
│   │   │   ├── endpoints.py
│   │   │   └── router.py
│   │   ├── models.py
│   │   └── views.py
│   │
│   ├── patients/                   # Gestão de pacientes
│   │   ├── api/
│   │   │   ├── endpoints.py
│   │   │   ├── router.py
│   │   │   └── schemas.py
│   │   ├── models.py
│   │   └── views.py
│   │
│   ├── evaluations/               # Avaliações neuropsicológicas
│   │   ├── api/
│   │   │   ├── endpoints.py
│   │   │   ├── router.py
│   │   │   └── schemas.py
│   │   ├── models.py
│   │   └── views.py
│   │
│   ├── tests/                     # Testes psicológicos (WISC-IV, BPA2, etc)
│   │   ├── api/
│   │   │   ├── endpoints.py       # API REST dos testes
│   │   │   ├── router.py
│   │   │   └── schemas.py
│   │   ├── models.py              # Application, TestResult
│   │   ├── views.py
│   │   ├── services/
│   │   │   └── scoring_service.py  # Lógica de cálculo
│   │   ├── wisc4/
│   │   │   ├── calculators.py     # Cálculos WISC-IV
│   │   │   ├── classifiers.py     # Classificações
│   │   │   ├── interpreters.py    # Interpretações
│   │   │   ├── paths.py
│   │   │   └── __init__.py        # Módulo WISC-IV
│   │   │   └── tabelas/           # Tabelas normativas
│   │   │       ├── Equivalentes das somas dos pontos ponderados/
│   │   │       │   ├── Tabela-GAI.csv
│   │   │       │   ├── Tabela-CPI.csv
│   │   │       │   ├── Tabela A2.csv ... A6.csv
│   │   │       ├── tabelas-cd/
│   │   │       ├── tabelas-a8/
│   │   │       └── tabelas-ncp/
│   │   ├── bpa2/                  # Teste BPA-2
│   │   ├── ebadep_a/              # Teste EBADEP-A
│   │   └── ebaped_ij/             # Teste EBAPED-IJ
│   │
│   ├── reports/                   # Laudos e relatórios
│   │   └── models.py
│   │
│   ├── api/                       # API principal (Ninja)
│   │   ├── auth.py                # Autenticação JWT
│   │   ├── router.py              # Router principal
│   │   └── views.py
│   │
│   └── common/                    # Componentes compartilhados
│
├── config/                        # Configurações Django
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── config/                        # Templates HTML (atual)
│   ├── templates/
│   │   ├── base/
│   │   │   └── base.html          # Layout base com sidebar
│   │   ├── dashboard/
│   │   ├── patients/
│   │   ├── evaluations/
│   │   ├── tests/
│   │   └── reports/
│   │
│   └── static/                    # CSS compilado
│       └── css/dist/styles.css
│
├── theme/                         # Tema Tailwind
│   └── static_src/
│       ├── src/input.css
│       ├── tailwind.config.js
│       └── package.json
│
└── manage.py


neuro-frontend/                   # Projeto Next.js (Frontend)
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── layout.tsx
│   │
│   ├── (dashboard)/
│   │   ├── patients/
│   │   │   ├── page.tsx           # Lista pacientes
│   │   │   ├── [id]/
│   │   │   │   └── page.tsx       # Detalhes paciente
│   │   │   └── new/
│   │   │       └── page.tsx
│   │   │
│   │   ├── evaluations/
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   │       └── page.tsx
│   │   │
│   │   ├── tests/
│   │   │   ├── page.tsx           # Lista testes
│   │   │   ├── wisc4/
│   │   │   │   ├── page.tsx      # Form WISC-IV
│   │   │   │   └── [id]/result/page.tsx  # Resultado
│   │   │   ├── bpa2/
│   │   │   └── ...
│   │   │
│   │   ├── reports/
│   │   │   └── page.tsx
│   │   │
│   │   └── layout.tsx            # Layout com sidebar
│   │
│   ├── api/
│   │   └── auth/
│   │       └── [...nextauth]/route.ts
│   │
│   ├── layout.tsx
│   └── page.tsx
│
├── components/
│   ├── ui/                        # Componentes base
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   ├── Table.tsx
│   │   ├── Badge.tsx
│   │   └── Modal.tsx
│   │
│   ├── layout/
│   │   ├── Sidebar.tsx
│   │   ├── Header.tsx
│   │   └── PageHeader.tsx
│   │
│   ├── patients/
│   │   ├── PatientList.tsx
│   │   ├── PatientForm.tsx
│   │   └── PatientCard.tsx
│   │
│   ├── evaluations/
│   │   ├── EvaluationCard.tsx
│   │   └── EvaluationForm.tsx
│   │
│   ├── tests/
│   │   ├── wisc4/
│   │   │   ├── SubtestInput.tsx
│   │   │   ├── IndexTable.tsx
│   │   │   ├── ResultSummary.tsx
│   │   │   └── GAI_CPI_Card.tsx
│   │   └── common/
│   │       ├── TestSelector.tsx
│   │       └── ScoreInput.tsx
│   │
│   └── reports/
│       └── ReportViewer.tsx
│
├── lib/
│   ├── api.ts                     # Fetch wrapper
│   ├── auth.ts                    # NextAuth config
│   └── utils.ts                   # Helpers
│
├── services/
│   ├── patientService.ts
│   ├── evaluationService.ts
│   ├── wisc4Service.ts
│   └── reportService.ts
│
├── types/
│   ├── patient.ts
│   ├── evaluation.ts
│   ├── wisc4.ts
│   └── index.ts
│
├── hooks/
│   ├── usePatients.ts
│   ├── useWISC4.ts
│   └── useAuth.ts
│
├── public/
│   └── images/
│
├── .env.local
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

## Fluxo de Dados

```
Usuário
   │
   ▼
┌─────────────────────────────────────────────┐
│              Next.js (Frontend)             │
│  ┌─────────┐  ┌──────────┐  ┌───────────┐  │
│  │  Pages  │  │Components│  │  Services │  │
│  └────┬────┘  └────┬─────┘  └─────┬─────┘  │
│       │            │              │         │
│       └────────────┴──────────────┘         │
│                    │                         │
│                    ▼                         │
│             lib/api.ts (fetch)               │
└────────────────────┬─────────────────────────┘
                     │ HTTP JSON
                     ▼
┌─────────────────────────────────────────────┐
│           Django (Backend)                  │
│  ┌─────────────────────────────────────┐    │
│  │         Django Ninja API            │    │
│  │   apps/patients/api/endpoints.py   │    │
│  │   apps/tests/api/endpoints.py      │    │
│  └──────────────┬──────────────────────┘    │
│                 │                            │
│  ┌──────────────┴──────────────────────┐     │
│  │           Django ORM                │     │
│  │    models.py + scoring_service.py  │     │
│  └─────────────────────────────────────┘     │
└─────────────────────────────────────────────┘
```

## Endpoints API (Atual + Futuros)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/patients/` | Lista pacientes |
| POST | `/api/patients/` | Cria paciente |
| GET | `/api/patients/{id}/` | Detalhes paciente |
| PUT | `/api/patients/{id}/` | Atualiza paciente |
| DELETE | `/api/patients/{id}/` | Remove paciente |
| GET | `/api/evaluations/` | Lista avaliações |
| POST | `/api/evaluations/` | Cria avaliação |
| GET | `/api/tests/wisc4/` | Info WISC-IV |
| POST | `/api/tests/wisc4/calculate/` | Calcula WISC-IV |
| GET | `/api/tests/wisc4/result/{id}/` | Resultado WISC-IV |
| GET | `/api/reports/` | Lista laudos |
| POST | `/api/auth/login/` | Login JWT |
| POST | `/api/auth/refresh/` | Refresh token |

## Tecnologias

| Camada | Tecnologia |
|--------|------------|
| Backend | Django 4+ |
| API | Django Ninja |
| Frontend | Next.js 14 (App Router) |
| UI | Tailwind CSS |
| Auth | NextAuth.js + JWT |
| State | React Query (opcional) |
| Deploy | Vercel (frontend) + Railway/Render (backend) |