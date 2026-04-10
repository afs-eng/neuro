# Frontend Structure

## Visao Geral

O frontend principal fica em `neuro-frontend/` e usa `Next.js 14` com `App Router`, `React`, `TypeScript` e `Tailwind CSS`.

O projeto esta organizado por areas funcionais do dashboard e por camadas simples:

- `app/` para rotas e layouts
- `components/` para interface reutilizavel
- `services/` para acesso a API Django
- `lib/` para infraestrutura compartilhada
- `types/` para contratos TypeScript

## Estrutura Atual

```text
neuro-frontend/
├── app/
│   ├── dashboard/
│   │   ├── accounts/
│   │   │   └── page.tsx
│   │   ├── ai/
│   │   │   └── page.tsx
│   │   ├── documents/
│   │   │   └── page.tsx
│   │   ├── evaluations/
│   │   │   ├── page.tsx
│   │   │   ├── new/
│   │   │   │   └── page.tsx
│   │   │   └── [id]/
│   │   │       ├── layout.tsx
│   │   │       ├── page.tsx
│   │   │       ├── edit/page.tsx
│   │   │       ├── overview/page.tsx
│   │   │       ├── progress/page.tsx
│   │   │       ├── documents/page.tsx
│   │   │       ├── tests/page.tsx
│   │   │       ├── report/page.tsx
│   │   │       └── anamnesis/
│   │   │           ├── page.tsx
│   │   │           ├── new/page.tsx
│   │   │           └── [anamnesisId]/page.tsx
│   │   ├── patients/
│   │   │   ├── page.tsx
│   │   │   ├── new/page.tsx
│   │   │   └── [id]/page.tsx
│   │   ├── reports/
│   │   │   ├── page.tsx
│   │   │   ├── [id]/page.tsx
│   │   │   └── generate/[evaluationId]/page.tsx
│   │   ├── tests/
│   │   │   ├── page.tsx
│   │   │   ├── bpa2/
│   │   │   ├── ebadep-a/
│   │   │   ├── ebadep-ij/
│   │   │   ├── epq-j/
│   │   │   ├── etdah-ad/
│   │   │   ├── etdah-pais/
│   │   │   ├── fdt/
│   │   │   ├── ravlt/
│   │   │   ├── scared/
│   │   │   ├── srs2/
│   │   │   └── wisc4/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── public/
│   │   └── anamnesis/[token]/page.tsx
│   ├── forgot-password/page.tsx
│   ├── login/page.tsx
│   ├── register/page.tsx
│   ├── reset-password/page.tsx
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── anamnesis/
│   │   ├── AnamnesisResponseViewer.tsx
│   │   ├── FieldRenderer.tsx
│   │   ├── FormStepRenderer.tsx
│   │   ├── InternalAnamnesisEditor.tsx
│   │   ├── ProgressHeader.tsx
│   │   ├── RepeaterField.tsx
│   │   ├── ReviewSummary.tsx
│   │   └── types.ts
│   ├── evaluations/
│   │   ├── EvaluationHeader.tsx
│   │   └── EvaluationTabs.tsx
│   ├── layout/
│   │   ├── AppHeader.tsx
│   │   ├── AppLayout.tsx
│   │   ├── AppSidebar.tsx
│   │   └── SystemLayout.tsx
│   ├── tests/
│   │   └── wisc4/
│   └── ui/
│       ├── avatar.tsx
│       ├── badge.tsx
│       ├── button.tsx
│       ├── card.tsx
│       ├── dropdown-menu.tsx
│       ├── input.tsx
│       ├── page.tsx
│       ├── progress.tsx
│       ├── scroll-area.tsx
│       ├── select.tsx
│       ├── separator.tsx
│       ├── table.tsx
│       └── tabs.tsx
├── lib/
│   ├── api.ts
│   └── utils.ts
├── services/
│   ├── anamnesisService.ts
│   ├── documentService.ts
│   ├── evaluationService.ts
│   ├── index.ts
│   ├── patientService.ts
│   ├── reportService.ts
│   ├── testService.ts
│   └── wisc4Service.ts
├── types/
│   ├── evaluation.ts
│   ├── index.ts
│   ├── patient.ts
│   └── tests/
│       └── wisc4.ts
├── package.json
├── postcss.config.js
├── tailwind.config.ts
└── tsconfig.json
```

## Organizacao de Rotas

### Rotas publicas

- `/login`
- `/register`
- `/forgot-password`
- `/reset-password`
- `/public/anamnesis/[token]`

### Rotas autenticadas

Todas as telas de operacao ficam sob `app/dashboard/` e usam `app/dashboard/layout.tsx`, que encapsula o `AppLayout`.

As principais areas sao:

- `patients`: cadastro e consulta de pacientes
- `evaluations`: ciclo principal da avaliacao
- `tests`: aplicacao e visualizacao de instrumentos
- `reports`: geracao e leitura de laudos
- `documents`: anexos da avaliacao
- `accounts`: area administrativa
- `ai`: superficie de recursos assistivos

## Layout e Navegacao

O layout autenticado usa tres componentes centrais:

- `components/layout/AppLayout.tsx`: casca principal do dashboard
- `components/layout/AppSidebar.tsx`: navegacao lateral
- `components/layout/AppHeader.tsx`: cabecalho superior

Hoje o controle visual da sidebar acontece no cliente via `useState`, dentro do proprio `AppLayout`.

## Integracao com a API

O frontend conversa diretamente com o backend Django por meio de `lib/api.ts`.

Responsabilidades dessa camada:

- resolver a base URL da API
- anexar token JWT salvo em `localStorage`
- tratar `FormData` e JSON
- normalizar mensagens de erro
- expor helpers `get`, `post`, `put`, `patch` e `delete`

Exemplo de uso:

```ts
import { api } from '@/lib/api'

export const testService = {
  getInstruments: () => api.get<any[]>('/api/tests/instruments/'),
  addApplication: (evaluationId: number, instrumentId: number) =>
    api.post('/api/tests/applications/', {
      evaluation_id: evaluationId,
      instrument_id: instrumentId,
    }),
}
```

## Services

Os `services/` concentram o consumo dos endpoints do backend e evitam espalhar chamadas HTTP nas paginas.

- `patientService.ts`: pacientes
- `evaluationService.ts`: avaliacoes e progresso
- `anamnesisService.ts`: templates, respostas e fluxo publico/interno
- `documentService.ts`: upload e listagem de anexos
- `reportService.ts`: laudos e geracao
- `testService.ts`: instrumentos e aplicacoes
- `wisc4Service.ts`: operacoes especificas do WISC-IV

## Padrao das Paginas de Testes

As paginas de testes seguem um padrao simples:

- pagina raiz do instrumento para aplicacao ou entrada
- pagina `[id]/page.tsx` para detalhes/edicao quando necessario
- pagina `[id]/result/page.tsx` para leitura clinica do resultado

Instrumentos atualmente expostos no frontend:

- `bpa2`
- `ebadep-a`
- `ebadep-ij`
- `epq-j`
- `etdah-ad`
- `etdah-pais`
- `fdt`
- `ravlt`
- `scared`
- `srs2`
- `wisc4`

## Observacoes Arquiteturais

- O frontend atual e majoritariamente client-side nas telas do dashboard.
- A autenticacao no browser depende do token salvo localmente.
- Existe uma base de componentes `ui/` reutilizavel com Radix UI e utilitarios de estilo.
- A pasta `components/tests/wisc4/` existe, mas hoje a maior parte da tela de resultado esta implementada diretamente na rota correspondente.
- O frontend novo convive com telas legadas renderizadas pelo proprio Django no backend.

## Stack do Frontend

- Next.js 14.1
- React 18
- TypeScript 5
- Tailwind CSS 3
- Radix UI
- TanStack React Query (instalado, uso parcial)
- Axios (instalado, mas a camada principal atual usa `fetch` em `lib/api.ts`)
