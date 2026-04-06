# Estrutura do Frontend Next.js

```
neuro-frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── layout.tsx
│   │
│   ├── (dashboard)/
│   │   ├── patients/
│   │   │   ├── page.tsx          # Lista pacientes
│   │   │   ├── [id]/
│   │   │   │   └── page.tsx      # Detalhes paciente
│   │   │   └── new/
│   │   │       └── page.tsx      # Novo paciente
│   │   │
│   │   ├── evaluations/
│   │   │   ├── page.tsx          # Lista avaliações
│   │   │   └── [id]/
│   │   │       └── page.tsx      # Detalhes avaliação
│   │   │
│   │   ├── tests/
│   │   │   ├── page.tsx          # Lista testes disponíveis
│   │   │   ├── wisc4/
│   │   │   │   ├── page.tsx      # Form WISC-IV
│   │   │   │   └── [id]/
│   │   │   │       └── result.tsx  # Resultado WISC-IV
│   │   │   ├── etdah-ad/
│   │   │   │   ├── page.tsx      # Form ETDAH-AD
│   │   │   │   └── [id]/
│   │   │   │       └── result.tsx  # Resultado ETDAH-AD
│   │   │   ├── etdah-pais/
│   │   │   │   ├── page.tsx      # Form ETDAH-PAIS
│   │   │   │   └── [id]/
│   │   │   │       └── result.tsx  # Resultado ETDAH-PAIS
│   │   │   └── ...
│   │   │
│   │   ├── reports/
│   │   │   └── page.tsx          # Lista laudos
│   │   │
│   │   └── layout.tsx            # Layout com sidebar
│   │
│   ├── api/
│   │   └── auth/
│   │       └── [...nextauth]/    # NextAuth handlers
│   │
│   ├── layout.tsx                # Root layout
│   └── page.tsx                  # Redirect para dashboard
│
├── components/
│   ├── ui/                       # Componentes reutilizáveis
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   ├── Table.tsx
│   │   ├── Modal.tsx
│   │   └── ...
│   │
│   ├── layout/
│   │   ├── Sidebar.tsx
│   │   ├── Header.tsx
│   │   └── SidebarItem.tsx
│   │
│   ├── patients/
│   │   ├── PatientList.tsx
│   │   ├── PatientCard.tsx
│   │   └── PatientForm.tsx
│   │
│   ├── tests/
│   │   ├── WISC4/
│   │   │   ├── SubtestForm.tsx
│   │   │   ├── IndexTable.tsx
│   │   │   └── ResultChart.tsx
│   │   └── ...
│   │
│   └── reports/
│       └── ReportViewer.tsx
│
├── lib/
│   ├── api.ts                   # Fetch wrapper
│   ├── auth.ts                  # Auth utilities
│   └── utils.ts                 # Helpers
│
├── types/
│   ├── patient.ts
│   ├── evaluation.ts
│   ├── wisc4.ts
│   └── ...
│
├── services/                    # Chamadas API específicas
│   ├── patientService.ts
│   ├── evaluationService.ts
│   └── wisc4Service.ts
│
├── tailwind.config.ts
├── next.config.js
├── package.json
└── tsconfig.json
```

## Arquivos Principais

### lib/api.ts - Fetch wrapper
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = await getToken()
  
  const res = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  })

  if (!res.ok) {
    throw new Error(`API Error: ${res.status}`)
  }

  return res.json()
}

// Helper methods
export const api = {
  get: <T>(url: string) => fetchAPI<T>(url),
  post: <T>(url: string, data: unknown) => 
    fetchAPI<T>(url, { method: 'POST', body: JSON.stringify(data) }),
  put: <T>(url: string, data: unknown) => 
    fetchAPI<T>(url, { method: 'PUT', body: JSON.stringify(data) }),
  delete: <T>(url: string) => 
    fetchAPI<T>(url, { method: 'DELETE' }),
}
```

### services/patientService.ts
```typescript
import { api } from '@/lib/api'

export interface Patient {
  id: number
  full_name: string
  birth_date: string
  sex: string
  schooling?: string
}

export const patientService = {
  list: () => api.get<Patient[]>('/api/patients/'),
  
  get: (id: number) => api.get<Patient>(`/api/patients/${id}/`),
  
  create: (data: Partial<Patient>) => 
    api.post<Patient>('/api/patients/', data),
  
  update: (id: number, data: Partial<Patient>) => 
    api.put<Patient>(`/api/patients/${id}/`, data),
  
  delete: (id: number) => api.delete(`/api/patients/${id}/`),
}
```

### app/(dashboard)/patients/page.tsx
```typescript
import { patientService } from '@/services/patientService'
import { PatientList } from '@/components/patients/PatientList'

export default async function PatientsPage() {
  const patients = await patientService.list()
  
  return (
    <div>
      <div className="flex justify-between mb-6">
        <h1 className="text-2xl font-semibold">Pacientes</h1>
        <a href="/patients/new" className="btn btn-primary">
          Novo Paciente
        </a>
      </div>
      <PatientList patients={patients} />
    </div>
  )
}
```

### .env.local
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key
```

## Instalação

```bash
npx create-next-app@latest neuro-frontend
# Escolher: TypeScript, Tailwind, App Router

cd neuro-frontend
npm install @tanstack/react-query axios next-auth
```

## Integração com Django

1. **CORS** - Configure em Django (`django-cors-headers`)
2. **Auth** - Use JWT ou Session auth
3. **API** - Sua API já existe em `apps/tests/api/`

Quer que eu crie alguns arquivos de exemplo para começar?
