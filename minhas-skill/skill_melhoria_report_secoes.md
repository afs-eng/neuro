# SKILL — MELHORIA DA CAMADA DE REPORT POR SEÇÕES NO SISTEMA NEUROPSICOLÓGICO

## OBJETIVO

Aprimorar a arquitetura atual de geração de seções do laudo neuropsicológico, mantendo o pipeline já existente no sistema e tornando-o mais:

- previsível
- modular
- auditável
- escalável
- resiliente
- fácil de manter

A melhoria deve respeitar a arquitetura atual baseada em:

- endpoint de regeneração de seção
- `ReportSectionService`
- `snapshot_builder`
- `ReportAIService`
- `TextGenerationService`
- fallback determinístico
- persistência de conteúdo, metadata, warnings e histórico

O objetivo não é substituir esse fluxo, mas **padronizar e fortalecer a geração de cada seção do laudo**.

## CONTEXTO ATUAL DO SISTEMA

O fluxo atual funciona assim:

1. o endpoint recebe a solicitação de regeneração de uma seção
2. valida permissão e busca o laudo
3. chama `ReportSectionService.regenerate_section(...)`
4. o serviço localiza a seção pelo `section_key`
5. reconstrói o snapshot clínico atual da avaliação
6. verifica se a seção suporta IA
7. se suportar IA, tenta gerar via prompt específico
8. se houver erro, cai para fallback determinístico
9. salva conteúdo, metadata, warnings e histórico
10. recompõe o laudo consolidado

Essa arquitetura já está correta.  
A melhoria deve se concentrar em **formalizar o comportamento de cada seção**.

## PRINCÍPIO CENTRAL

Cada `section_key` do laudo deve passar a ter uma definição explícita contendo:

- suporte ou não a IA
- dados exigidos no snapshot
- dados opcionais
- prompt específico
- regras de filtragem de contexto
- fallback determinístico
- formato textual esperado
- regras clínicas de redação
- metadados obrigatórios
- políticas de warning

## META DA MELHORIA

Transformar a geração das seções em um mecanismo orientado por configuração e contratos, evitando:

- lógica espalhada
- comportamento inconsistente entre seções
- prompts mal definidos
- fallback fraco
- contexto excessivo enviado para IA
- falta de padronização clínica

## RESULTADO ESPERADO

Ao final da melhoria, cada seção do laudo deverá ser gerada com base em uma especificação formal, permitindo que o sistema:

- saiba exatamente quais dados cada seção usa
- envie apenas o contexto necessário para IA
- tenha fallback determinístico equivalente
- produza seções com estrutura clínica consistente
- registre geração e falhas com clareza
- facilite criação de novas seções

## ARQUITETURA ALVO

A arquitetura deve continuar usando os mesmos serviços centrais, porém com uma nova camada de definição de seções.

### Estrutura proposta

```text
apps/reports/
  api/
    endpoints.py

  services/
    report_section_service.py
    report_ai_service.py
    report_generation_service.py
    section_registry.py
    section_context_service.py
    section_validation_service.py

  builders/
    snapshot_builder.py

  prompts/
    base_system_prompt.txt
    sections/
      bpa2_prompt.txt
      fdt_prompt.txt
      ravlt_prompt.txt
      wisc4_prompt.txt
      conclusao_prompt.txt

  fallbacks/
    bpa2_fallback.py
    fdt_fallback.py
    ravlt_fallback.py
    wisc4_fallback.py
    conclusao_fallback.py

  contracts/
    section_contracts.py
```

## COMPONENTES A IMPLEMENTAR OU APRIMORAR

### 1. `section_registry.py`
Criar um registro central das seções.

Esse registro deve descrever o comportamento completo de cada `section_key`.

### Exemplo conceitual

```python
SECTION_REGISTRY = {
    "bpa2": {
        "label": "BPA-2",
        "supports_ai": True,
        "prompt_name": "sections/bpa2_prompt.txt",
        "required_snapshot_paths": [
            "patient",
            "evaluation",
            "validated_tests.bpa2"
        ],
        "optional_snapshot_paths": [
            "anamnese",
            "clinical_evolution"
        ],
        "fallback_builder": "build_bpa2_fallback",
        "expected_output_type": "rich_text_section",
        "category": "test_section"
    }
}
```

## O REGISTRY DEVE DEFINIR

Para cada seção:

- `section_key`
- nome amigável
- categoria da seção
- se suporta IA
- nome do prompt
- campos obrigatórios do snapshot
- campos opcionais do snapshot
- validador de dados mínimos
- fallback correspondente
- ordem da seção no laudo
- política de warning
- regras especiais de persistência, se houver

## 2. `section_context_service.py`
Criar um serviço responsável por filtrar o snapshot bruto.

### Objetivo
Receber o snapshot completo e devolver apenas o contexto necessário para a seção.

### Responsabilidades
- ler o contrato da seção
- validar presença de dados mínimos
- montar JSON enxuto para IA
- remover ruído desnecessário
- evitar envio excessivo de contexto
- padronizar estrutura para todos os prompts

### Exemplo
Se a seção for `bpa2`, enviar:
- dados do paciente
- dados da avaliação
- resultados do BPA-2
- trechos de anamnese relevantes
- trechos de evolução clínica relevantes

Não enviar:
- todos os testes irrelevantes
- todos os documentos sem relação
- dados redundantes que poluem o prompt

## 3. `section_validation_service.py`
Criar uma validação formal de contexto mínimo por seção.

### Objetivo
Antes de tentar IA ou fallback, garantir que a seção possui os dados necessários.

### Deve validar
- se o teste exigido existe
- se os resultados validados existem
- se o snapshot tem dados suficientes
- se a seção pode ser regenerada naquele momento

### Benefício
Evita prompts vazios, erros silenciosos e textos fracos por falta de contexto.

## 4. `contracts/section_contracts.py`
Formalizar contratos de entrada e saída das seções.

### Contrato mínimo por seção
Cada seção deve declarar:

- dados mínimos de entrada
- estrutura esperada do contexto filtrado
- estratégia de geração
- política de fallback
- formato de conteúdo final

## CONTRATO DE ENTRADA

Cada seção deve receber:

```python
{
    "report": "...",
    "section_key": "bpa2",
    "snapshot": {...},
    "filtered_context": {...},
    "user": {...}
}
```

## CONTRATO DE SAÍDA

A geração da seção deve devolver um resultado padronizado:

```python
{
    "content_generated": "texto final da seção",
    "generation_metadata": {
        "provider": "openai",
        "model": "modelo-usado",
        "finish_reason": "stop",
        "usage": {...},
        "section": "bpa2",
        "prompt_name": "sections/bpa2_prompt.txt"
    },
    "warnings_payload": [],
    "used_fallback": False
}
```

Quando houver fallback:

```python
{
    "content_generated": "texto final determinístico",
    "generation_metadata": {
        "provider": "deterministic",
        "model": "rules-based",
        "section": "bpa2",
        "fallback_reason": "erro bruto da IA"
    },
    "warnings_payload": [
        "A IA não está disponível no momento. O conteúdo foi gerado pelo modo determinístico."
    ],
    "used_fallback": True
}
```

## 5. PROMPTS POR SEÇÃO
Cada seção com suporte por IA deve possuir um prompt próprio.

### Regra
Os prompts devem sair de um modelo genérico e passar a seguir uma estrutura uniforme.

### Estrutura recomendada de prompt
Cada prompt de seção deve conter:

1. objetivo clínico da seção
2. papel da IA
3. dados que serão recebidos
4. estrutura textual obrigatória
5. restrições de escrita
6. proibições
7. estilo técnico do laudo
8. regra de não inventar dados
9. regra de usar apenas o contexto enviado
10. instruções de saída limpa

## EXEMPLO DE ESTRUTURA PARA PROMPT DE SEÇÃO

```text
Objetivo:
Gerar a seção do BPA-2 do laudo neuropsicológico com base exclusivamente nos dados estruturados recebidos.

Você deve:
- redigir em linguagem técnica
- manter coerência clínica
- descrever os resultados do instrumento
- interpretar cada domínio avaliado
- finalizar com síntese clínica
- utilizar a expressão “Em análise clínica” no fechamento interpretativo
- não inventar escores, percentis, classificações ou sintomas

Estrutura obrigatória:
1. parágrafo introdutório do instrumento
2. interpretação de cada domínio
3. síntese clínica final

Restrições:
- não usar travessões longos
- não criar subtítulos fora do padrão solicitado
- não mencionar testes não incluídos no contexto
- não citar dados ausentes
```

## 6. FALLBACKS DETERMINÍSTICOS POR SEÇÃO
Cada seção deve ter um fallback robusto, não genérico.

### Regra
O fallback não deve ser apenas um texto mínimo.  
Ele deve reproduzir, dentro do possível, a mesma estrutura clínica da versão por IA.

### Exemplo
Se a seção `bpa2` exige:
- introdução
- interpretação de AC
- interpretação de AD
- interpretação de AA
- interpretação de AG
- síntese final

Então o fallback também deve devolver exatamente isso.

## 7. PADRONIZAÇÃO TEXTUAL DAS SEÇÕES
Todas as seções devem seguir o padrão de escrita do projeto.

### Regras obrigatórias
- linguagem técnica
- coerência clínica
- sem repetição excessiva
- sem travessões longos
- sem invenção de dados
- sem citar paciente pelo nome completo nas análises, salvo regra específica
- fechamento interpretativo com “Em análise clínica”, conforme padrão do projeto
- estrutura estável entre gerações

## 8. DATA PRESENCE GUARD MAIS ESTRUTURADO
O `DataPresenceGuard` deve ser expandido para funcionar por contrato de seção.

### Deve verificar
- presença do teste exigido
- presença dos escores necessários
- presença de anamnese, quando a seção exigir
- presença de evolução, quando for relevante
- completude mínima para geração por IA

### Se faltar contexto
Deve:
- registrar warning claro
- impedir prompt pobre
- acionar fallback ou bloqueio controlado

## 9. MELHORIA DO `ReportSectionService`
O `ReportSectionService` deve continuar como orquestrador principal, mas com responsabilidades melhor delimitadas.

### Fluxo ideal revisado

1. localizar seção
2. validar bloqueio
3. reconstruir snapshot
4. carregar contrato da seção
5. validar dados mínimos
6. filtrar contexto com serviço dedicado
7. decidir IA ou fallback
8. gerar conteúdo
9. persistir metadata, warnings e histórico
10. recompôr laudo consolidado

## 10. SEPARAÇÃO ENTRE ORQUESTRAÇÃO E REGRAS
Hoje o serviço central pode estar acumulando decisões demais.

### Melhor prática
- `ReportSectionService`: orquestração
- `section_registry.py`: definição da seção
- `section_context_service.py`: filtragem de contexto
- `section_validation_service.py`: validação de dados mínimos
- `ReportAIService`: geração por IA
- `fallbacks/*.py`: regras determinísticas por seção

## 11. METADATA MAIS RICA
Padronizar a metadata salva em cada geração.

### Campos recomendados
- `provider`
- `model`
- `section`
- `prompt_name`
- `finish_reason`
- `usage`
- `used_fallback`
- `fallback_reason`
- `generated_at`
- `context_version`
- `snapshot_hash`
- `section_contract_version`

## Benefício
Isso melhora:
- auditoria
- rastreabilidade
- debug
- comparação entre versões
- controle de regressão

## 12. WARNINGS MAIS CLAROS
Padronizar `warnings_payload`.

### Exemplos úteis
- IA indisponível, fallback utilizado
- contexto clínico parcialmente ausente
- teste validado ausente na avaliação
- seção gerada com dados mínimos insuficientes
- parte da anamnese não encontrada

## 13. HISTÓRICO MELHOR VERSIONADO
Cada regeneração deve registrar:
- conteúdo anterior
- conteúdo novo
- provider usado
- modelo usado
- se houve fallback
- erro bruto resumido
- versão do contrato da seção

## 14. PROMPT BASE MAIS ENXUTO
O `base_system_prompt.txt` deve conter apenas as regras gerais do sistema.

### Não colocar no prompt base
- instruções específicas de BPA-2
- instruções de FDT
- instruções de conclusão
- detalhes de estrutura de uma seção específica

### O prompt base deve conter
- estilo técnico do laudo
- proibição de inventar dados
- regra de usar apenas o contexto
- padrão clínico global do sistema

## 15. PROMPTS ESPECÍFICOS MAIS OBJETIVOS
Os prompts específicos devem ser focados na seção.  
Evitar prompts longos demais e difusos.

### Cada prompt deve dizer claramente
- o que a seção precisa produzir
- em qual estrutura
- com quais dados
- com quais limites

## 16. SAÍDA CONTROLADA
Idealmente, a IA deve devolver apenas o texto final da seção, sem:
- cabeçalhos extras não solicitados
- explicações meta
- listas indevidas
- comentários sobre ausência de contexto, a menos que isso seja exigido

## 17. TESTES AUTOMATIZADOS
Criar testes para o fluxo de regeneração de seções.

### Cobrir
- seção com IA funcionando
- seção com IA falhando
- seção sem suporte por IA
- seção com contexto incompleto
- seção bloqueada
- persistência de metadata
- persistência de warnings
- criação de histórico
- reconstrução do laudo consolidado

## 18. BOAS PRÁTICAS DE IMPLEMENTAÇÃO
- evitar lógica de prompt espalhada em múltiplos arquivos sem contrato
- evitar contextos gigantes enviados ao provider
- evitar fallback genérico único para tudo
- evitar depender de texto livre para lógica posterior
- manter cada seção autocontida por contrato

## 19. BENEFÍCIOS DA MELHORIA
A adoção dessa arquitetura traz:

- mais estabilidade na geração
- mais controle por seção
- mais qualidade nos textos
- menos erro por contexto ruim
- mais facilidade para adicionar novos testes
- melhor manutenção do sistema
- melhor observabilidade em produção

## 20. OBJETIVO FINAL DA IMPLEMENTAÇÃO
Após essa melhoria, o sistema deverá ser capaz de regenerar qualquer seção do laudo de forma robusta, seguindo este princípio:

- cada seção conhece seu contrato
- cada seção sabe quais dados precisa
- cada seção sabe qual prompt usar
- cada seção sabe como cair em fallback
- cada seção salva histórico e metadata padronizados
- o laudo final se recompõe de modo consistente

## INSTRUÇÃO FINAL
Implemente a melhoria da camada de report baseada em contratos por seção, preservando o pipeline atual do sistema, mas formalizando registry, filtragem de contexto, validação de dados mínimos, prompts específicos, fallbacks determinísticos e metadata padronizada para cada `section_key` do laudo.
