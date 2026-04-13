# NeuroAvalia - Skills do Projeto

## Visão Geral do Projeto

NeuroAvalia é um sistema de gestão de avaliações neuropsicológicas completo, desenvolvido com arquitetura full-stack moderna. O sistema permite o gerenciamento de pacientes, avaliações clínicas, aplicação de instrumentos psicológicos padronizados, geração de laudos e integração com funcionalidades assistivas de IA.

O projeto foi concebido para atender clínicas de neuropsicologia e profissionais da área de saúde mental, oferecendo uma plataforma digital que organiza todo o fluxo de trabalho clínico - desde o cadastro de pacientes até a emissão de laudos detalhados.

A arquitetura segue o padrão de monólito modular orientado a domínio, onde o backend Django concentra toda a lógica de negócio, persistência e regras clínicas, enquanto o frontend Next.js acts exclusivamente como interface de apresentação. Esta separação clara de responsabilidades garante que o backend permaneça como fonte oficial da verdade para todos os dados clínicos, incluindo escores calculados, percentis, classificações e interpretações.

O sistema é nativamente preparado para evolução futura com mensageria (Celery + Redis), permitindo processamento assíncrono de tarefas intensivas como cálculo de normas complexas, geração de PDFs em background e integração com APIs externas.

## Stack Oficial do Projeto

### Backend

O backend é construído sobre Django 4+, utilizando Django Ninja para construção de APIs RESTful modernas e eficientes. Esta escolha tecnológica permite endpoint declarativos com validação automática de schemas Pydantic, gerando documentação OpenAPI automaticamente e oferecendo performance superior comparada a abordagens tradicionais baseadas em Django REST Framework.

A camada de banco de dados utiliza PostgreSQL em produção como fonte oficial de verdade, garantindo robustez, escalabilidade e suporte a tipos de dados complexos. Em desenvolvimento, SQLite é utilizado para facilitar a configuração local, mantendo compatibilidade através do Django ORM.

O sistema de autenticação utiliza JWT (JSON Web Tokens) com refresh tokens persistidos no banco, oferecendo segurança robusta sem necessidade de sessões server-side. A autorização segue modelo de papéis (roles) com permissões granulares por recurso.

### Frontend

O frontend utiliza Next.js 14 com App Router, oferecendo renderização híbrida server-side e client-side. A interface é construída com Tailwind CSS, garantindo consistência visual e responsividade. O state management pode utilizar React Query para data fetching, mantendo cache e sincronização automática com o backend.

A camada de comunicação com a API é centralizada em `lib/api.ts`, evitando duplicação de código e garantindo tratamento consistente de erros, headers de autenticação e formatação de requisições.

### Infraestrutura

O projeto inclui configurações Docker completas para desenvolvimento e produção, com docker-compose orquestrando backend, frontend e banco de dados. A infraestrutura está preparada para evolução futura com Redis (cache e message broker), workers Celery (tarefas assíncronas), e Nginx (reverse proxy e load balancing).

## Arquitetura Oficial

### Organização Macro do Backend

O backend Django está organizado em aplicações (apps) por domínio de negócio, seguindo princípio de responsabilidade única e coesão. Cada app representa um contexto delimitado do sistema, contendo seus próprios modelos, serviços, selectors e endpoints de API.

```
apps/
├── accounts/          # Gestão de usuários e autenticação
├── ai/                # Camada de IA assistiva (LangChain)
├── anamnesis/         # Questionários de anamnese
├── api/               # API principal (Ninja)
├── audit/             # Auditoria de ações críticas
├── common/            # Componentes compartilhados
├── documents/         # Gestão de documentos e arquivos
├── evaluations/       # Avaliações neuropsicológicas
├── messaging/         # Sistema de mensagens internas
├── patients/          # Gestão de pacientes
├── reports/           # Laudos e relatórios
└── tests/            # Instrumentos psicológicos (NÚCLEO CLÍNICO)
```

Cada app segue estrutura interna padronizada quando aplicável:

```
apps/<app_name>/
├── models/           # Modelos Django (quando necessário)
├── api/             # Endpoints Ninja
├── services/        # Lógica de negócio
├── selectors.py     # Consultas ao banco
├── validators.py    # Validações de entrada
├── permissions.py   # Permissões específicas
├── workflows.py     # Fluxos complexos (quando necessário)
└── apps.py         # Configuração do app
```

### Organização Macro do Frontend

O frontend Next.js está organizado por rotas e componentes, seguindo convenções do App Router:

```
neuro-frontend/
├── app/
│   ├── dashboard/    # Área autenticada
│   │   ├── patients/
│   │   ├── evaluations/
│   │   ├── tests/
│   │   ├── reports/
│   │   ├── documents/
│   │   ├── ai/
│   │   ├── accounts/
│   │   └── anamnesis/
│   ├── login/       # Autenticação
│   └── page.tsx     # Landing page
├── components/
│   ├── ui/          # Componentes base
│   ├── layout/      # Sidebar, Header, etc
│   ├── patients/    # Componentes específicos
│   ├── tests/       # Componentes de testes
│   └── anamnesis/   # Componentes de anamnese
├── lib/
│   ├── api.ts       # Cliente HTTP
│   └── utils.ts     # Helpers
├── services/        # Serviços de domínio
└── types/           # Tipos TypeScript
```

### Padrão de Dados entre Backend e Frontend

A comunicação segue protocolo HTTP JSON padrão:

```
Frontend (Next.js)
    │
    ├── Requisições HTTP GET/POST/PUT/DELETE
    ├── Headers: Authorization: Bearer <token>
    └── Body: JSON (schemas Pydantic)
           │
           ▼
Backend (Django Ninja)
    │
    ├── Validação de schemas
    ├── Autorização (permissions)
    ├── Lógica de negócio (services)
    ├── Persistência (Django ORM)
    └── Resposta JSON
```

## Princípios Obrigatórios

### Fonte da Verdade

O backend Django é a fonte oficial e exclusiva de verdade para todos os dados clínicos. Esta é a regra mais fundamental do sistema: qualquer cálculo, classificação, interpretação ou decisão que afete dados de pacientes deve obrigatoriamente passar pelo backend. O frontend nunca deve realizar cálculos normativos, aplicações de tabelas de normas, ou decisões clínicas de qualquer natureza.

Esta separação garante que auditoria, versionamento, segurança e consistência dos dados sejam mantidos centralizadamente. Além disso, permite que múltiplos clientes (web, mobile, API externa) consumam os mesmos dados com as mesmas regras de negócio, evitando duplicação de lógica crítica.

### Separação Clínica de Dados

Toda aplicação de instrumento psicológico deve seguir estrutura de dados padronizada que separa claramente os estágios de processamento:

- **raw_payload**: Dados brutos digitados pelo avaliador, sem qualquer processamento. Este campo almacena a entrada原始 exatamente como recebida do frontend.

- **computed_payload**: Resultado do processamento pelo backend, contendo escores calculados, pontos ponderados, percentis e valores derivados das tabelas normativas. Este campo é gerado exclusivamente pelo backend.

- **classified_payload**: Classificação clínica baseada nos valores computados. Segue padrões internacionais de classificação (muy superior, superior, médio, limítrofe, etc.).

- **interpretation_text**: Interpretação textual gerada pelos interpretadores dos instrumentos. Pode ser assistida por IA, mas sempre revisada por profissional.

Esta separação permite auditoria completa do processo de avaliação, rastreabilidade de alterações e reprocessamento quando necessário.

### IA como Camada Assistiva

A inteligência artificial no sistema existe exclusivamente como camada assistiva, nunca substitutiva. A IA pode auxiliar na organização de dados, sugestão de resumos, recomendação de estrutura de laudos, e tradução de conceitos técnicos. Porém, a IA nunca pode calcular escores, aplicar normas, classificar resultados ou emitir qualquer tipo de julgamento clínico definitivo.

O profissional sempre permanece como autoridade final sobre qualquer decisão clínica. A IA serve como ferramenta de produtividade, não como substituto do julgamento humano.

### Segurança em Camadas

A segurança é implementada em múltiplas camadas:

- **Autenticação**: JWT com refresh tokens, expiração configurável, invalidação no logout.
- **Autorização**: Permissões granulares por papel e recurso.
- **Auditoria**: Registro de todas as ações críticas em log de auditoria.
- **Proteção de Dados**: Criptografia em trânsito (HTTPS), validação de entrada, sanitização de saída.
- **Camada de IA**: Guards específicos para validar inputs e outputs de IA.

## Papel do Módulo Tests

O módulo `tests` é o núcleo clínico do sistema, responsável por todo o processamento de instrumentos psicológicos. Este é o componente mais crítico do backend, contendo a lógica determinística que calcula escores, aplica normas internacionais e gera classificações clínicas.

### Estrutura do Módulo

O módulo está organizado em subdirectórios por instrumento, cada qual com sua própria implementação específica:

```
apps/tests/
├── base/                    # Tipos e interfaces compartilhadas
│   ├── types.py            # TestContext, ComputedScore, etc
│   ├── interfaces.py       # Protocolos (ICalculator, IClassifier)
│   └── exceptions.py       # Exceções customizadas
├── models/                  # Modelos Django do domínio
│   ├── instruments.py      # Instrument (catálogo de instrumentos)
│   ├── applications.py    # TestApplication (aplicação de teste)
│   └── templates.py        # InterpretationTemplate
├── services/               # Serviços centrais
│   ├── application_service.py
│   ├── scoring_service.py
│   └── interpretation_service.py
├── selectors.py            # Consultas ao banco
├── registry.py             # Registro de instrumentos
├── api/                    # Endpoints Ninja
├── norms/                  # Tabelas normativas
└── instrumentos/           # Módulos por instrumento
    ├── wisc4/             # WISC-IV
    ├── bpa2/              # BPA-2
    ├── ebadep_a/          # EBADEP-A
    ├── ebaped_ij/         # EBAPED-IJ
    ├── epq_j/             # EPQ-J
    ├── etdah_ad/          # ETAH-AD
    ├── fdt/               # FDT
    └── ravlt/              # RAVLT
```

### Instrumentos Suportados

O sistema atualmente suporta os seguintes instrumentos psicológicos:

| Código | Nome Completo | Faixa Etária |
|--------|---------------|--------------|
| wisc4 | Wechsler Intelligence Scale for Children - 4ª Edição | 6-16 anos |
| bpa2 | Bateria Psicológica para Avaliação - 2ª Edição | Adulto |
| ebadep_a | Escala Brasileira de Autismo - Adulto | Adulto |
| ebaped_ij | Escala Brasileira de Autismo - Infantojuvenil | 2-18 anos |
| epq_j | Questionário de Personalidade para Jovens | 7-15 anos |
| etdah_ad | Escala de Transtorno de Hiperatividade - Adulto | Adulto |
| fdt | Teste de Fluência Verbal | 5+ anos |
| ravlt | Rey Auditory Verbal Learning Test | 16+ anos |

Cada instrumento implementa interface padronizada com métodos de validação, cálculo, classificação e interpretação, garantindo consistência no fluxo de processamento independentemente do instrumento específico.

## Papel da Camada AI

A camada de IA (`apps.ai`) existe como módulo isolado do restante da lógica de negócio, serving exclusivamente como ferramenta assistiva. Esta separação garante que a IA não tenha acesso direto ao banco de dados, não realize cálculos normativos e não tome decisões clínicas.

### Estrutura da Camada

```
apps/ai/
├── api/          # Endpoints Ninja para geração de texto
├── services/     # AIService principal
├── providers/    # Implementações de provedores (OpenAI, Anthropic)
├── chains/       # LangChain chains customizadas
├── prompts/      # Templates de prompt centralizados
├── guards/       # Validadores de input e output
├── logging/      # Sistema de logs específico
└── schemas/      # Schemas Pydantic
```

### Responsabilidades

A camada de IA é responsável por:

- Receber dados estruturados do backend (nunca dados brutos)
- Processar requisições de geração de texto
- Aplicar guardrails de segurança
- Registrar logs para auditoria
- Retornar sugestões ao frontend

A camada NÃO é responsável por:

- Cálculo de escores ou percentis
- Aplicação de tabelas normativas
- Classificação clínica
- Decisões de diagnóstico
- Acesso direto ao banco de dados

## Diretriz de Evolução com Mensageria

A arquitetura está preparada para evolução futura com Celery + Redis. Esta preparação inclui:

### Estrutura de Tarefas Assíncronas

Quando necessário, o sistema poderá delegar as seguintes operações para workers assíncronos:

- Processamento de instrumentos com grande volume de dados
- Geração de PDFs de laudos
- Envio de emails e notificações
- Integração com APIs externas
- Processamento em lote de avaliações
- Operações de backup automatizado

### Configuração de Ambiente

O ambiente está pronto para receber:

```
# docker-compose.yml (futuro)
services:
  redis:
    image: redis:7-alpine
  worker:
    build: .
    command: celery -A config worker -l info
  beat:
    command: celery -A config beat -l info
```

A adição de Celery será transparente para o código existente, utilizando a mesma estrutura de serviços já implementada.

## Diretrizes de Desenvolvimento

### Boas Práticas de Backend

- Toda lógica de negócio deve estar em services
- Models devem conter apenas definição de campos e métodos de instância
-Selectors devem encapsular queries complexas
- Validators validam entrada antes de passar para services
- API endpoints devem ser thin wrappers sobre services

### Boas Práticas de Frontend

- Zero lógica clínica determinística
- Zero cálculos normativos
- Zero armazenamento de dados sensíveis em estado local
- Toda comunicação via API centralizada
- Tipagem forte com TypeScript

### Boas Práticas de Segurança

- Validação de entrada em todas as APIs
- Sanitização de saída para evitar XSS
- Criptografia de dados sensíveis em trânsito e em repouso
- Rate limiting em endpoints críticos
- Auditoria de todas as ações sensíveis

## Começando com o Projeto

### Configuração Local

1. Criar ambiente virtual Python
2. Instalar dependências: `pip install -r requirements.txt`
3. Configurar variáveis de ambiente (copiar .env.example)
4. Executar migrações: `python manage.py migrate`
5. Criar superusuário: `python manage.py createsuperuser`
6. Iniciar servidor: `python manage.py runserver`

### Executando Frontend

1. cd neuro-frontend
2. Instalar dependências: `npm install`
3. Configurar .env.local
4. Executar: `npm run dev`

### Docker Compose (Desenvolvimento)

```bash
docker-compose up --build
```

Este comando inicia todos os serviços necessários: backend, frontend, banco de dados.

## Referências

- DOCUMENTAÇÃO ADICIONAL: `PROJECT_ARCHITECTURE.md`
- REGRAS DE NEGÓCIO: `SKILLS_REGRAS_NEGOCIO.md`
- SEGURANÇA: `SKILLS_SEGURANCA.md`
- INTELIGÊNCIA ARTIFICIAL: `SKILLS_IA.md`
