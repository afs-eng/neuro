# Inteligência Artificial - NeuroAvalia

## Visão Geral

Este documento define a arquitetura, princípios, restrições e implementação da camada de Inteligência Artificial do sistema NeuroAvalia. A IA no NeuroAvalia existe exclusivamente como ferramenta assistiva de produtividade, nunca como substituta do julgamento clínico profissional.

A implementação da IA segue o princípio fundamental de que o profissional de neuropsicologia permanece como autoridade final sobre todas as decisões clínicas. O sistema foi desenhado para utilizar IA como copiloto que organiza, sugere e auxiliary, mas nunca decide. Esta abordagem protege tanto o paciente quanto o profissional, garantindo que a tecnologia amplie a capacidade humana sem substituir o discernimento clínico.

A camada de IA está isolada em um módulo dedicado (apps.ai), separado do restante da lógica de negócio. Este isolamento garante que a IA não tenha acesso direto ao banco de dados, não realize cálculos normativos, não tome decisões clínicas e não persista dados sem supervisão.

## Princípios Fundamentais

### IA é Assistiva, Não Determinística

A inteligência artificial no NeuroAvalia serve exclusivamente como assistente de produtividade. Ela pode ajudar a organizar informações, sugerir estruturas de texto, resumir dados e traduzir conceitos, mas nunca toma decisões clínicasIndependentes.

Esta distinção entre "assistir" e "decidir" é fundamental para a segurança do sistema. A IA processa dados que já foram validados e calculados pelo backend, gerando sugestões que são apresentadas ao profissional para revisão. O profissional sempre tem a oportunidade de editar, rejeitar ou ignorar qualquer sugestão da IA.

### IA Não Calcula Escores

O cálculo de escores, percentis, pontos ponderados e qualquer valor normativo é exclusivamente responsabilidade do backend. A IA não participa deste processo de forma alguma.

Esta separação é crítica porque os cálculos normativos seguem algoritmos determinísticos com regras claras e tabelas definidas. Qualquer erro在这些 cálculos pode ter implicações clínicas significativas, então eles permanecem sob controle humano rigoroso.

O fluxo correto é:

```
Frontend → API (dados brutos) → Backend (calcula escores) → Banco (persiste)
                                                            ↓
                                          IA recebe dados processados
                                                            ↓
                                          Gera sugestões
                                                            ↓
                                          Profissional revisa
```

### IA Não Aplica Normas

As tabelas normativas são aplicadas exclusivamente pelo backend. Cada instrumento (WISC-IV, BPA-2, etc) possui suas próprias tabelas normativas específicas para idade e escolaridade, e estas são implementadas deterministicamente no código do backend.

A IA não tem acesso a estas tabelas e não pode aplicá-las. Ela recebe os resultados já calculados (escore, percentil, classificação) e pode apenas auxiliar na interpretação ou organização textual desses resultados.

### IA Não Substitui Revisão Humana

Toda e qualquer saída da IA passa por revisão obrigatória antes de ser incorporada ao sistema. O profissional é responsável por validar, editar e aprovar qualquer conteúdo sugerido pela IA.

O sistema impede que outputs da IA sejam automaticamente incorporados sem supervisão. Mesmo que a IA gere um texto aparentemente correto, ele é marcado como "rascunho gerado por IA" e requer aprovação explícita do profissional.

## Arquitetura da Camada de IA

### Visão Geral da Estrutura

A camada de IA está isolada em apps.ai, seguindo arquitetura modular que separa responsabilidades:

```
apps/ai/
├── api/              # Endpoints Ninja para requisições
├── services/         # AIService - lógica principal
├── providers/        # Implementações de provedores
├── chains/           # LangChain chains customizadas
├── prompts/          # Templates de prompt centralizados
├── guards/           # Validadores de input/output
├── logging/          # Sistema de logs específico
└── schemas/          # Request/Response schemas Pydantic
```

### Responsabilidades de Cada Módulo

#### API (apps.ai.api)

Responsável por expor endpoints REST para geração de texto:

- Receber requisições do frontend
- Validar schemas de entrada
- Chamar AIService com parâmetros corretos
- Retornar respostas formatadas
- Aplicar rate limiting

#### Service (apps.ai.services)

Responsável pela lógica de negócio da IA:

- Orquestrar o fluxo de geração
- Selecionar prompt correto baseado na tarefa
- Aplicar guardrails
- Tratar erros e exceções
- Registrar logs

#### Providers (apps.ai.providers)

Responsável pela comunicação com provedores de IA:

- Abstração de diferentes APIs (OpenAI, Anthropic)
- Tratamento de rate limits dos provedores
- Retry com backoff exponencial
- Timeout e cancelamento
- Fallback para provedores alternativos

#### Chains (apps.ai.chains)

Responsável por definir fluxos de processamento específicos:

- Chains customizadas para cada tipo de tarefa
- Integração com LangChain
- Composição de múltiplos passos
- Memória e contexto

#### Prompts (apps.ai.prompts)

Responsável por centralizar templates de prompt:

- Templates em arquivos separados
- Versionamento de prompts
- Testes A/B de diferentes versões
- Localização (futuro)

#### Guards (apps.ai.guards)

Responsável pela validação de segurança:

- Validar que output não contém decisões clínicas
- Sanitizar output
- Verificar limites de tamanho
- Detectar conteúdo sensível

#### Logging (apps.ai.logging)

Responsável pelo registro de interações:

- Log de todas as requisições
- Métricas de uso
- Detecção de anomalias
- Auditoria

## Providers Desacoplados

O sistema suporta múltiplos provedores de IA de forma intercambiável:

### Interface Comum

```python
class BaseProvider(Protocol):
    def generate(self, prompt: str, **kwargs) -> str: ...
    def generate_structured(self, schema: dict, prompt: str, **kwargs) -> dict: ...
    @property
    def model(self) -> str: ...
    @property
    def max_tokens(self) -> int: ...
```

### Provedores Suportados

#### OpenAI

```python
class OpenAIProvider(BaseProvider):
    def __init__(self, model: str = "gpt-4", api_key: str = None):
        self.model = model
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    
    def generate(self, prompt: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2048)
        )
        return response.choices[0].message.content
```

#### Anthropic

```python
class AnthropicProvider(BaseProvider):
    def __init__(self, model: str = "claude-3-sonnet-20240229", api_key: str = None):
        self.model = model
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    
    def generate(self, prompt: str, **kwargs) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", 2048),
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
```

### Configuração

```python
# config/settings/base.py
AI_CONFIG = {
    "provider": env("AI_PROVIDER", "openai"),
    "model": env("AI_MODEL", "gpt-4"),
    "temperature": env.float("AI_TEMPERATURE", 0.7),
    "max_tokens": env.int("AI_MAX_TOKENS", 2048),
    "enabled": env.bool("AI_ENABLED", True),
}
```

## Prompts Centralizados

Todos os prompts são centralizados em apps.ai.prompts, facilitando manutenção e versionamento:

### Estrutura de Prompts

```
prompts/
├── base/
│   └── system.txt           # Instruções base do sistema
├── tasks/
│   ├── summarize.txt       # Resumir dados
│   ├── suggest.txt         # Sugerir recomendações
│   ├── draft.txt           # Criar rascunho
│   ├── translate.txt       # Traduzir termos
│   ├── explain.txt        # Explicar conceitos
│   └── review.txt         # Revisar consistência
└── tests/
    ├── interpretation.txt  # Interpretar resultados
    └── report_structure.txt  # Estruturar laudo
```

### Exemplo de Prompt

```txt
# prompts/tasks/summarize.txt

Você é assistente especializado em avaliações neuropsicológicas.
Sua tarefa é resumir os resultados de forma clara e profissional.

Instruções:
1. Use linguagem técnica apropriada para profissionais de neuropsicologia
2. Destaque achados relevantes
3. Mantenha objetividade
4. Não emita diagnósticos ou recomendações definitivas

Contexto adicional:
{context}

Resultados a resumir:
{results}

Lembre-se: Este é um resumo assistivo. A decisão final deve ser sempre do profissional.
```

### Carregamento de Prompts

```python
class PromptLoader:
    @staticmethod
    def load_task_prompt(task_type: str) -> str:
        path = Path(__file__).parent / "tasks" / f"{task_type}.txt"
        return path.read_text()
    
    @staticmethod
    def render(prompt: str, **kwargs) -> str:
        return prompt.format(**kwargs)
```

## Chains Organizadas

As chains LangChain são organizadas por tipo de tarefa:

### Chain de Sumarização

```python
class SummarizeChain:
    def __init__(self, provider: BaseProvider):
        self.provider = provider
        self.prompt_template = PromptLoader.load_task_prompt("summarize")
    
    def run(self, data: dict, context: dict = None) -> str:
        prompt = PromptLoader.render(
            self.prompt_template,
            results=json.dumps(data, indent=2),
            context=json.dumps(context or {}, indent=2)
        )
        return self.provider.generate(prompt, temperature=0.5)
```

### Chain de Sugestão

```python
class SuggestChain:
    def __init__(self, provider: BaseProvider):
        self.provider = provider
        self.prompt_template = PromptLoader.load_task_prompt("suggest")
    
    def run(self, profile: dict, context: dict = None) -> str:
        prompt = PromptLoader.render(
            self.prompt_template,
            profile=json.dumps(profile, indent=2),
            context=json.dumps(context or {}, indent=2)
        )
        return self.provider.generate(prompt, temperature=0.7)
```

### Chain de Rascunho

```python
class DraftChain:
    def __init__(self, provider: BaseProvider):
        self.provider = provider
        self.prompt_template = PromptLoader.load_task_prompt("draft")
    
    def run(self, data: dict, template: str = None) -> str:
        prompt = PromptLoader.render(
            self.prompt_template,
            data=json.dumps(data, indent=2),
            template=template or "padrão"
        )
        return self.provider.generate(prompt, temperature=0.7)
```

## Guardrails

Os guardrails são validações críticas que garantem que a IA opere dentro de limites seguros:

### Tipos de Guardrails

#### Validação de Decisões Clínicas

```python
class AIGuard:
    FORBIDDEN_TERMS = [
        "diagnóstico",
        "diagnóstico final",
        "prescrição",
        "tratamento definitivo",
        "classificação clínica definitiva",
        "resultado final",
        "decisão clínica",
        "prescrever",
        "indicado para tratamento",
    ]
    
    @classmethod
    def validate_no_clinical_decision(cls, output: str) -> tuple[bool, list[str]]:
        warnings = []
        output_lower = output.lower()
        for term in cls.FORBIDDEN_TERMS:
            if term in output_lower:
                warnings.append(f"Termo sensível detectado: {term}")
        
        return len(warnings) == 0, warnings
```

#### Validação de Dados de Entrada

```python
    @classmethod
    def validate_data_safety(cls, data: dict) -> tuple[bool, list[str]]:
        warnings = []
        sensitive_fields = ["cpf", "rg", "endereço", "telefone", "email"]
        
        for field in sensitive_fields:
            if field in data and data[field]:
                warnings.append(f"Campo sensível encontrado: {field}")
        
        return len(warnings) == 0, warnings
```

#### Limite de Tamanho

```python
    @classmethod
    def check_output_length(cls, output: str, max_chars: int = 10000) -> tuple[bool, str]:
        if len(output) > max_chars:
            return False, f"Output excede {max_chars} caracteres"
        return True, ""
```

#### Sanitização

```python
    @classmethod
    def sanitize_output(cls, output: str) -> str:
        output = output.strip()
        output = re.sub(r'\s+', ' ', output)
        output = re.sub(r'[^\w\s.,;:\-()\[\]{}áàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ]', '', output)
        return output
```

### Aplicação de Guardrails

```python
class AIService:
    def generate(self, task_type: str, data: dict, context: dict = None) -> dict:
        # Validação de input
        safe_input, input_warnings = AIGuard.validate_data_safety(data)
        if not safe_input:
            raise ValueError(f"Dados sensíveis detectados: {input_warnings}")
        
        # Obter provider
        provider = self._get_provider()
        
        # Selecionar chain
        chain = self._get_chain(task_type)
        
        # Gerar output
        output = chain.run(data, context)
        
        # Validação de output
        safe_output, output_warnings = AIGuard.validate_no_clinical_decision(output)
        if not safe_output:
            AILogger.log_guard_violation("clinical_decision", output_warnings)
            raise ValueError(f"Output contém decisões clínicas: {output_warnings}")
        
        length_ok, length_msg = AIGuard.check_output_length(output)
        if not length_ok:
            raise ValueError(length_msg)
        
        output = AIGuard.sanitize_output(output)
        
        # Log
        AILogger.log_response(task_type, True, len(output), output_warnings)
        
        return {
            "output": output,
            "warnings": input_warnings + output_warnings,
        }
```

## Logs e Rastreabilidade

### Sistema de Logging

Toda interação com IA é registrada para auditoria:

```python
class AILogger:
    @staticmethod
    def log_request(task_type: str, input_data_keys: list, user_id: int = None, ip: str = None):
        logger.info(
            f"AI Request - task: {task_type}, user: {user_id}, ip: {ip}, "
            f"data_keys: {input_data_keys}, timestamp: {datetime.utcnow().isoformat()}"
        )
    
    @staticmethod
    def log_response(task_type: str, success: bool, output_length: int, warnings: list = None):
        if success:
            logger.info(
                f"AI Response - task: {task_type}, output_length: {output_length}, "
                f"warnings: {warnings}, timestamp: {datetime.utcnow().isoformat()}"
            )
        else:
            logger.error(
                f"AI Error - task: {task_type}, error: {error}, "
                f"timestamp: {datetime.utcnow().isoformat()}"
            )
```

### O que é Logado

| Campo | Descrição |
|-------|-----------|
| timestamp | Data e hora da requisição |
| user_id | ID do usuário que solicitou |
| ip_address | Endereço IP do cliente |
| task_type | Tipo de tarefa solicitada |
| input_data_keys | Chaves dos dados de entrada (não valores) |
| output_length | Tamanho do output gerado |
| success | Se a requisição foi bem-sucedida |
| warnings | Avisos gerados pelos guards |
| provider | Provider utilizado |
| model | Modelo utilizado |

### O que NÃO é Logado

- Valores de dados sensíveis (CPF, endereço, etc)
- Resultados de testes
- Dados de pacientes
- Histórico clínico

## Tipos de Tarefas Suportadas

| Task Type | Descrição | Exemplo de Uso |
|-----------|-----------|----------------|
| summarize | Resumir dados | Resumir resultados de múltiplos testes |
| suggest | Sugerir recomendações | Recomendações baseadas em perfil |
| draft | Criar rascunho | Rascunho de laudo |
| translate | Traduzir termos | Converter termos técnicos para linguagem acessível |
| explain | Explicar conceitos | Explicar classificação de resultados |
| review | Revisar consistência | Verificar consistência de laudo |

### Fluxo por Tarefa

```
1. Frontend: Usuário solicita ajuda da IA
2. API: Recebe task_type + dados processados
3. Service: Valida inputs, seleciona prompt
4. Chain: Executa com dados estruturados
5. Guard: Valida output
6. Service: Registra log
7. API: Retorna para frontend
8. Frontend: Exibe para revisão
9. Usuário: Revisa, edita, aprova
10. Se aprovado: Texto é incorporado
```

## Integração com Backend

### Fluxo de Integração

A IA só pode ser chamada através de endpoint seguro do backend:

```python
# apps.ai.api.endpoints
@router.post("/generate/")
def generate_ai(
    request: HttpRequest,
    task: str = Body(..., embed=True),
    data: dict = Body(...),
    context: dict = Body(default=None),
):
    # 1. Autenticação
    if not request.user.is_authenticated:
        raise Http404("Unauthorized")
    
    # 2. Permissão
    if not request.user.has_perm("ai:generate"):
        raise PermissionDenied()
    
    # 3. Rate limiting (aplicado pelo middleware)
    
    # 4. Obter dados processados (não brutos)
    # A IA recebe dados que já foram validados e processados pelo backend
    
    # 5. Chamar serviço
    result = AIService.generate(task, data, context)
    
    # 6. Retornar
    return result
```

### Dados Recebidos pela IA

A IA recebe apenas dados já processados:

```python
# Exemplo: dados processados para sugestão de laudo
data = {
    "patient_name": "João Silva",  # Apenas nome, não CPF
    "age": 10,
    "evaluation_date": "2024-01-15",
    "instruments_applied": ["wisc4", "bpa2"],
    "results_summary": {
        "wisc4": {"qi_total": 95, "classification": "médio"},
        "bpa2": {"classification": "normal"}
    },
    "clinical_observations": "Paciente apresentou..."
}
```

A IA NÃO recebe:

- Dados brutos (raw_payload)
- CPFs ou identificadores pessoais
- Dados raw de respostas
- Tabelas normativas

## Restrições de Uso

### Limites Técnicos

| Limite | Valor | Justificativa |
|--------|-------|---------------|
| Rate limit | 10 req/min/usuário | Prevenir abuso |
| Timeout | 30 segundos | Evitar queries longas |
| Max input | 50KB | Prevenir DoS |
| Max output | 10KB | Controlar custos |
| Concurrent requests | 3 por usuário | Recursos finitos |

### Limites de Conteúdo

A IA está programada para:

- ✅ Resumir dados processados
- ✅ Sugerir estrutura de laudo
- ✅ Traduzir termos técnicos
- ✅ Explicar conceitos estatísticos
- ✅ Revisar texto quanto à consistência

A IA NÃO deve:

- ❌ Emitir diagnósticos
- ❌ Sugerir tratamentos
- ❌ Classificar resultados
- ❌ Calcular escores
- ❌ Aplicar normas
- ❌ Decidir sobre pacientes

## Preparação para Celery

A arquitetura está preparada para processamento assíncrono de IA:

### Tarefas Celery (Futuro)

```python
# apps.ai.tasks
@celery_app.task
def generate_ai_async(task_type: str, data: dict, context: dict, callback_url: str):
    result = AIService.generate(task_type, data, context)
    
    # Notificar frontend quando completo
    if callback_url:
        requests.post(callback_url, json=result)
    
    return result
```

### Benefícios

- Não bloqueia requisições HTTP
- Permite retry automático
- Rate limiting mais fino
- Controle de custos
- Monitoramento de uso

## Configuração de Ambiente

### Variáveis Obrigatórias

```bash
# Habilitar/desabilitar IA
AI_ENABLED=true

# Provedor (openai, anthropic)
AI_PROVIDER=openai

# Modelo
AI_MODEL=gpt-4
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=2048

# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### Configuração por Instrumento

```python
AI_INSTRUMENT_CONFIGS = {
    "wisc4": {
        "enabled_tasks": ["summarize", "explain"],
        "max_output_tokens": 2048,
    },
    "bpa2": {
        "enabled_tasks": ["summarize", "suggest"],
        "max_output_tokens": 2048,
    },
    # ...
}
```

## Referências

- Visão Geral: `SKILLS.md`
- Regras de Negócio: `SKILLS_REGRAS_NEGOCIO.md`
- Segurança: `SKILLS_SEGURANCA.md`
- Arquitetura: `PROJECT_ARCHITECTURE.md`
