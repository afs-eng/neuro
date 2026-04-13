# SKILL - Implementacao da IA para Laudos no Sistema Neuro

## Objetivo

Implementar geracao assistida de laudos no sistema Neuro de forma clinicamente segura, incremental e aderente a arquitetura real do repositorio.

O objetivo nao e criar um modulo paralelo de laudos. O objetivo e evoluir o fluxo que ja existe em `apps/reports/`, usando `apps/ai/` como infraestrutura de IA reutilizavel.

Principio central:

- `apps/tests/` continua sendo o nucleo deterministico dos instrumentos.
- `apps/reports/` continua sendo o dono do workflow do laudo.
- `apps/ai/` passa a oferecer providers, prompts, guardrails e utilitarios de geracao.
- `neuro-frontend/` continua sendo a interface de geracao, revisao, regeneracao e finalizacao.

---

## Estado Real do Sistema

Hoje o sistema ja possui uma base forte para IA assistiva em laudos.

### Backend

O backend e modular e ja separa os dominios principais:

- `apps/patients/`
- `apps/evaluations/`
- `apps/anamnesis/`
- `apps/documents/`
- `apps/tests/`
- `apps/reports/`
- `apps/ai/`

### Modulo de testes

`apps/tests/` ja executa o fluxo clinico correto:

- validacao de dados brutos;
- calculo de escores;
- classificacao normativa;
- interpretacao textual do instrumento;
- persistencia em `TestApplication`.

Esse modulo e a fonte de verdade para resultado clinico. A IA nao deve recalcular nada aqui.

### Modulo de laudos

`apps/reports/` ja esta funcional e concentra o ciclo principal do laudo.

Hoje ele ja oferece:

- `Report`, `ReportSection` e `ReportVersion`;
- montagem de `context_payload` por snapshot da avaliacao;
- geracao completa por secoes;
- regeneracao por secao;
- edicao manual;
- versionamento;
- finalizacao;
- exportacao HTML e DOCX.

### Frontend

O frontend ja possui o fluxo base:

- tela para gerar laudo por avaliacao;
- tela para revisar secoes;
- salvar texto editado;
- regenerar secao;
- finalizar laudo;
- exportar.

### Camada de IA

`apps/ai/` ja existe no projeto, mas ainda e generica e pouco integrada ao fluxo de laudos.

Conclusao pratica:

O sistema nao precisa de um novo modulo de laudo com IA. Ele precisa conectar a infraestrutura de IA ao workflow que ja existe em `apps/reports/`.

---

## Regra Arquitetural

### 1. `apps/tests/` continua deterministico

Responsabilidades permanentes:

- validar payload bruto;
- calcular escore bruto e derivado;
- aplicar regra normativa;
- classificar percentil, escore ou faixa;
- gerar interpretacao tecnica por instrumento;
- persistir `TestApplication`.

A IA nao deve:

- calcular percentil;
- escolher norma;
- alterar classificacao;
- corrigir manual bruto;
- produzir resultado de teste ausente.

### 2. `apps/reports/` continua dono do caso de uso

Responsabilidades permanentes:

- montar o contexto clinico consolidado;
- decidir quais secoes existem no laudo;
- chamar geracao assistiva quando apropriado;
- persistir rascunho e secoes;
- manter versoes;
- controlar status;
- finalizar e exportar.

### 3. `apps/ai/` vira infraestrutura de IA

Responsabilidades desejadas:

- abstrair provider local e remoto;
- carregar prompts e regras;
- aplicar guardrails;
- registrar logs e metadados de geracao;
- retornar texto gerado de forma previsivel.

### 4. O frontend continua onde esta

O caminho recomendado nao e criar uma nova UX separada de IA.

O correto e evoluir as telas ja existentes em:

- `neuro-frontend/app/dashboard/reports/generate/[evaluationId]/page.tsx`
- `neuro-frontend/app/dashboard/reports/[id]/page.tsx`

---

## Arquitetura-Alvo Aderente ao Sistema

## 1. Camada clinica deterministica - `apps/tests/`

Cada instrumento deve continuar seguindo, quando possivel, o padrao:

```text
apps/tests/<instrumento>/
|- __init__.py
|- config.py
|- schemas.py
|- validators.py
|- calculators.py
|- classifiers.py
`- interpreters.py
```

### Evolucao recomendada

Os `interpreters.py` devem evoluir para produzir uma saida mais padronizada, mas sem quebrar o fluxo atual de persistencia.

Em vez de migrar tudo de uma vez, a recomendacao e introduzir um contrato progressivo.

Exemplo de alvo futuro por instrumento:

```python
{
    "instrument": "bpa2",
    "report_section": "atencao",
    "structured_results": {...},
    "clinical_interpretation": "...",
    "clinical_summary": {
        "global_status": "rebaixado",
        "main_weaknesses": ["atencao alternada"],
        "preserved_aspects": ["atencao dividida"],
        "flags": ["atencao_sustentada_reduzida"]
    }
}
```

Importante:

- isso e uma trilha de evolucao;
- nao deve bloquear a primeira fase da IA;
- o sistema ja consegue operar com `classified_payload`, `computed_payload`, `interpretation_text` e `result_rows`.

---

## 2. Workflow de laudo - `apps/reports/`

O modulo de laudos ja deve permanecer como orquestrador principal.

### Estrutura atual que deve ser preservada e expandida

```text
apps/reports/
|- api/
|- builders/
|- prompts/
|- services/
|- models.py
|- selectors.py
`- apps.py
```

### Servicos existentes que seguem validos

- `report_context_service.py`
- `report_generation_service.py`
- `report_section_service.py`
- `report_version_service.py`
- `report_validation_service.py`
- `report_export_service.py`

### Evolucao recomendada

Adicionar ou consolidar dentro de `apps/reports/services/`:

```text
apps/reports/services/
|- report_context_service.py
|- report_generation_service.py
|- report_section_service.py
|- report_version_service.py
|- report_validation_service.py
|- report_export_service.py
|- report_ai_service.py
`- report_review_service.py
```

#### `report_ai_service.py`

Responsabilidades:

- filtrar o contexto por secao;
- selecionar prompt;
- chamar `apps.ai`;
- normalizar warnings e metadados;
- devolver texto gerado e dados da geracao.

#### `report_review_service.py`

Responsabilidades:

- validar coerencia entre secoes;
- apontar dados ausentes;
- sinalizar hipotese diagnostica sem sustentacao;
- detectar contradicoes textuais obvias;
- registrar warnings de revisao.

---

## 3. Infraestrutura de IA - `apps/ai/`

`apps/ai/` nao deve ser dono da API de laudos. Ele deve ser uma camada transversal de IA.

### Estrutura recomendada

```text
apps/ai/
|- api/
|- guards/
|- logging/
|- prompts/
|- providers/
|- schemas/
|- services/
|- apps.py
`- __init__.py
```

### Estrutura alvo recomendada

```text
apps/ai/
|- guards/
|  |- data_presence_guard.py
|  |- diagnosis_guard.py
|  |- prompt_guard.py
|  `- safety_guard.py
|- logging/
|  `- ai_log_service.py
|- prompts/
|  |- base_system_prompt.txt
|  `- reports/
|     |- attention_prompt.txt
|     |- memory_prompt.txt
|     |- executive_functions_prompt.txt
|     |- conclusion_prompt.txt
|     |- hypothesis_prompt.txt
|     `- referrals_prompt.txt
|- providers/
|  |- base.py
|  |- ollama_provider.py
|  |- openai_provider.py
|  `- anthropic_provider.py
|- schemas/
|  |- generation_request.py
|  |- generation_response.py
|  `- provider_config.py
`- services/
   |- provider_factory.py
   |- prompt_registry_service.py
   `- text_generation_service.py
```

### Regra de ownership

- `apps/reports/` pergunta para `apps/ai` gerar texto;
- `apps/ai` nao cria `Report`, `ReportSection` ou `ReportVersion`;
- persistencia continua no dominio `reports`.

---

## Provider Strategy: Ollama Local + APIs Remotas

O sistema deve nascer provider-agnostic, mas com prioridade para uso local.

### Ordem recomendada

1. `ollama` como provider padrao;
2. `openai` como provider remoto opcional;
3. `anthropic` como provider remoto opcional.

### Motivos

#### Ollama local

Vantagens:

- maior privacidade;
- melhor aderencia a uso clinico sensivel;
- menor custo recorrente;
- ambiente controlado.

Limites:

- depende de hardware local;
- pode ter latencia maior em modelos grandes;
- qualidade varia conforme modelo escolhido.

#### APIs remotas

Vantagens:

- melhor qualidade em tarefas complexas;
- menor custo de manutencao operacional;
- fallback facil para casos mais pesados.

Limites:

- custo por uso;
- dependencia externa;
- maior cuidado com dados sensiveis.

### Interface base recomendada

`apps/ai/providers/base.py`

```python
from abc import ABC, abstractmethod


class BaseAIProvider(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, **kwargs) -> dict:
        raise NotImplementedError
```

Retorno recomendado:

```python
{
    "content": "texto gerado",
    "provider": "ollama",
    "model": "qwen2.5:14b",
    "finish_reason": "stop",
    "usage": {},
    "warnings": [],
}
```

### Configuracao sugerida

Adicionar no settings algo nesta linha:

```python
AI_PROVIDER = os.getenv("AI_PROVIDER", "ollama")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:14b")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL_TEXT = os.getenv("OPENAI_MODEL_TEXT", "gpt-4o")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL_TEXT = os.getenv("ANTHROPIC_MODEL_TEXT", "claude-3-7-sonnet-latest")
```

### Regra importante

O frontend nunca escolhe diretamente a chave nem fala com o provider.

Fluxo correto:

```text
Frontend -> /api/reports/... -> apps/reports -> apps/ai -> provider
```

---

## Contexto Clinico

O contexto ja existe hoje em forma de snapshot. A evolucao correta e melhorar esse snapshot, nao substitui-lo por outra camada paralela.

### Fonte unica de verdade

O contexto do laudo deve ser montado somente a partir de dados aprovados do sistema:

- paciente;
- avaliacao;
- anamnese atual;
- registros evolutivos marcados para laudo;
- documentos relevantes;
- testes validados;
- interpretacoes tecnicas dos instrumentos.

### Estrutura recomendada

O `context_payload` pode evoluir para algo como:

```python
{
    "patient": {...},
    "evaluation": {...},
    "anamnesis": {...},
    "documents": [...],
    "progress_entries": [...],
    "validated_tests": [...],
    "report_rules": {
        "use_first_name_only": True,
        "report_language": "pt-BR",
        "omit_raw_tables_in_text": True,
        "clinical_style": "tecnico_objetivo",
    },
}
```

### Regra de filtragem

O modelo nao deve receber todo o contexto bruto para toda secao.

Cada secao deve receber apenas o recorte necessario.

Exemplo:

- secao `atencao` recebe dados de BPA-2, E-TDAH e observacoes pertinentes;
- secao `memoria_aprendizagem` recebe RAVLT e dados relacionados;
- secao `hipotese_diagnostica` recebe sintese transversal, nunca payload bruto indiscriminado.

---

## Prompts e Guardrails

### Prompt base do sistema

`apps/ai/prompts/base_system_prompt.txt`

```text
Voce e um assistente tecnico de redacao de laudos neuropsicologicos.

Regras obrigatorias:
- Nao invente resultados.
- Nao altere classificacoes calculadas pelo sistema.
- Nao calcule escores, percentis ou normas.
- Use apenas os dados estruturados fornecidos.
- Quando faltarem dados, explicite a limitacao.
- Mantenha a resposta restrita a secao solicitada.
- Nao emita fechamento diagnostico autonomo.
- O texto deve ser formal, tecnico, objetivo e revisavel por humano.
```

### Prompt por secao

Cada secao clinica relevante deve ter prompt proprio.

Exemplo:

`apps/ai/prompts/reports/attention_prompt.txt`

```text
Redija exclusivamente a secao de Atencao do laudo.

Use apenas:
- resultados estruturados dos instrumentos atencionais;
- interpretacoes tecnicas ja fornecidas;
- observacoes clinicas relacionadas ao dominio;
- regras de estilo do laudo.

Nao cite valores crus desnecessarios.
Nao recalcule classificacoes.
Se os dados forem insuficientes, explicite a limitacao.

Retorne somente o texto final da secao.
```

### Guardrails minimos

#### `data_presence_guard.py`

- barra geracao de secao sem dados minimos;
- devolve warning claro ao usuario.

#### `diagnosis_guard.py`

- impede texto diagnostico categórico sem sustentacao;
- evita extrapolacao indevida;
- sinaliza contradicoes obvias.

#### `prompt_guard.py`

- garante que a entrada enviada ao provider siga o contrato esperado;
- reduz risco de prompt improvisado no codigo.

#### `safety_guard.py`

- aplica politicas gerais de saida;
- filtra resposta vazia, fora de escopo ou excessivamente especulativa.

---

## Modelagem de Persistencia

O modelo atual de `Report` ja e suficiente para iniciar a integracao.

### O que ja existe e deve ser aproveitado

- `status`
- `context_payload`
- `generated_text`
- `edited_text`
- `final_text`
- `ReportSection`
- `ReportVersion`

### Extensoes minimas recomendadas

Adicionar somente o que faltar para auditoria de IA.

Exemplo:

- `ai_metadata` em `Report` para metadados globais de geracao;
- `generation_metadata` em `ReportSection` para metadados por secao;
- `warnings_payload` em `ReportSection` para avisos de geracao ou revisao.

Exemplo conceitual:

```python
ai_metadata = models.JSONField(default=dict, blank=True)
generation_metadata = models.JSONField(default=dict, blank=True)
warnings_payload = models.JSONField(default=list, blank=True)
```

Evitar criar agora campos redundantes como:

- `draft_payload`
- `final_payload`
- `version` no proprio `Report`

Isso duplicaria estruturas ja resolvidas por `edited_text`, `final_text` e `ReportVersion`.

---

## API Recomendada

Como `reports` ja e o dominio dono do workflow, os endpoints devem continuar em `/api/reports/`.

### Manter e evoluir

Endpoints atuais validos:

- `POST /api/reports/generate-from-evaluation/{evaluation_id}`
- `POST /api/reports/{report_id}/build`
- `POST /api/reports/{report_id}/regenerate`
- `POST /api/reports/{report_id}/regenerate-section/{section_key}`
- `PATCH /api/reports/sections/{section_id}`
- `POST /api/reports/{report_id}/finalize`

### Possiveis extensoes

Sem quebrar o padrao atual, adicionar:

- `POST /api/reports/{report_id}/review-consistency`
- `POST /api/reports/{report_id}/generate-section/{section_key}` quando fizer sentido gerar secao isolada sem rebuild completo;
- `GET /api/reports/{report_id}/generation-metadata` se houver demanda de auditoria detalhada.

### Nao recomendado

Criar uma arvore paralela em `/api/ai/reports/...`.

Motivo:

- duplica ownership;
- espalha regra de negocio;
- enfraquece o dominio `reports`.

---

## Frontend

O frontend deve evoluir o que ja existe, nao criar outra superficie paralela.

### Telas principais

```text
neuro-frontend/app/dashboard/reports/generate/[evaluationId]/page.tsx
neuro-frontend/app/dashboard/reports/[id]/page.tsx
```

### Evolucoes recomendadas

#### Tela de geracao

- exibir se o provider ativo e local ou remoto;
- exibir warnings de dados ausentes antes da geracao;
- permitir escolher estrategia de geracao quando isso fizer sentido:
  - usar rascunho completo;
  - regenerar apenas secoes selecionadas.

#### Tela de revisao do laudo

- mostrar warnings por secao;
- indicar ultima geracao: provider, modelo e horario;
- permitir revisao de coerencia geral;
- manter fluxo atual de salvar, regenerar, finalizar e exportar.

### Service frontend

O caminho mais aderente e expandir `neuro-frontend/services/reportService.ts`, em vez de criar um `aiReportService.ts` paralelo sem necessidade.

---

## Fluxo Recomendado de Geracao

```text
Usuario
  -> abre avaliacao
  -> acessa geracao de laudo

Frontend
  -> chama endpoint existente de reports

apps/reports
  -> valida se ha dados minimos
  -> monta context_payload da avaliacao
  -> escolhe secoes elegiveis
  -> para cada secao decide:
     - texto deterministico
     - texto assistido por IA

apps/ai
  -> resolve provider configurado
  -> carrega prompt base + prompt da secao
  -> aplica guardrails
  -> chama Ollama ou API remota
  -> devolve texto + metadados + warnings

apps/reports
  -> persiste secoes
  -> atualiza versao do laudo
  -> devolve resposta ao frontend

Frontend
  -> exibe texto gerado
  -> permite editar
  -> permite regenerar secao
  -> permite revisar coerencia
  -> permite finalizar e exportar
```

---

## Fases de Implementacao

## Fase 1 - Infraestrutura minima real

### Backend

- implementar provider `ollama_provider.py` em `apps/ai/providers/`;
- implementar factory de provider;
- criar `base_system_prompt.txt`;
- criar `attention_prompt.txt`;
- integrar `apps/reports/services/report_section_service.py` com `apps/ai` para regeneracao real de uma secao;
- salvar metadados minimos da geracao.

### Frontend

- reaproveitar a tela atual do laudo;
- exibir sucesso, erro e warning de regeneracao por secao.

### Meta

Gerar com IA apenas uma secao real, preferencialmente `atencao`.

---

## Fase 2 - Expansao por secoes

- adicionar prompts para `memoria_aprendizagem`, `funcoes_executivas`, `conclusao`;
- permitir geracao assistida em mais de uma secao;
- adicionar `report_review_service.py` com checagens iniciais;
- armazenar warnings por secao.

### Meta

Ter secoes clinicas assistidas por IA com revisao humana e persistencia confiavel.

---

## Fase 3 - Contexto clinico melhorado

- padronizar melhor a saida de `interpreters.py` nos instrumentos mais usados;
- enriquecer `validated_tests` com `clinical_summary` mais consistente;
- reduzir dependencia de extracao generica de payloads heterogeneos.

### Meta

Melhorar qualidade do texto gerado sem mover calculo clinico para o LLM.

---

## Fase 4 - Multiprovider e auditoria

- habilitar OpenAI e Anthropic como fallback opcional;
- registrar provider, modelo, horario, usuario e warnings;
- implementar revisao de coerencia geral do laudo;
- melhorar observabilidade da geracao.

### Meta

Ter IA local como padrao e provedores remotos como opcao controlada.

---

## Fase 5 - Producao clinica madura

- revisar templates DOCX para aderencia ao novo fluxo;
- estabilizar criterios de pronto por secao;
- criar validacoes de seguranca e testes automatizados nos servicos de geracao;
- formalizar politica de uso de IA no processo clinico.

### Meta

Fechar o fluxo com seguranca clinica, rastreabilidade e manutencao simples.

---

## Criterios de Pronto

Esta implementacao sera considerada madura quando:

1. os testes continuarem sendo 100% determinísticos e independentes da IA;
2. o laudo continuar sendo gerenciado por `apps/reports`;
3. `apps/ai` suportar ao menos `ollama` e um provider remoto opcional;
4. a geracao por secao salvar metadados e warnings;
5. o frontend permitir revisar e editar tudo antes da finalizacao;
6. a exportacao final continuar funcionando com o texto aprovado;
7. o sistema conseguir sinalizar limitacoes de dados sem alucinacao textual evidente.

---

## Checklist Executivo

### Reports

- [ ] Integrar `report_section_service.py` com geracao real via `apps/ai`
- [ ] Criar `report_ai_service.py`
- [ ] Criar `report_review_service.py`
- [ ] Adicionar metadados minimos de IA nas secoes e/ou no laudo
- [ ] Manter versionamento e finalizacao no fluxo atual

### AI

- [ ] Criar `BaseAIProvider`
- [ ] Criar `ollama_provider.py`
- [ ] Criar `openai_provider.py`
- [ ] Criar `anthropic_provider.py`
- [ ] Criar `provider_factory.py`
- [ ] Criar `text_generation_service.py`
- [ ] Criar prompts base e por secao
- [ ] Criar `data_presence_guard.py`
- [ ] Criar `diagnosis_guard.py`
- [ ] Criar logging de geracao

### Tests

- [ ] Identificar instrumentos prioritarios para padronizacao de interpretacao
- [ ] Evoluir contrato de saida dos `interpreters.py` sem quebrar o fluxo atual

### Frontend

- [ ] Evoluir `reportService.ts`
- [ ] Exibir warnings de geracao
- [ ] Exibir metadados da ultima geracao
- [ ] Adicionar acao de revisao de coerencia quando backend suportar

---

## Resumo Final

O melhor encaixe para IA no sistema Neuro e este:

- `apps/tests/` permanece como motor clinico deterministico;
- `apps/reports/` permanece como dono do workflow do laudo;
- `apps/ai/` vira a infraestrutura de geracao textual, com Ollama local como padrao e APIs remotas como opcao;
- o frontend atual continua sendo a superficie de trabalho do profissional;
- a IA entra primeiro por secao, com revisao humana obrigatoria e rastreabilidade.

Essa abordagem reduz retrabalho, preserva a arquitetura real do sistema e permite evolucao incremental sem comprometer seguranca clinica.
