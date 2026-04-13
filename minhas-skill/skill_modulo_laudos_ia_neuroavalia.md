# SKILL — Implementação Completa do Módulo de Laudos com IA

## Objetivo
Implementar no sistema NeuroAvalia um módulo completo de **geração, edição, versionamento, exportação e envio de laudos com IA**, partindo de uma **avaliação já preenchida** com testes, anamnese e observações clínicas.

A implementação deve respeitar a arquitetura já existente do projeto, reaproveitando ao máximo os módulos atuais de pacientes, avaliações, testes, cálculo, classificação e interpretação.

O foco desta skill é transformar a avaliação finalizada em um **rascunho de laudo clínico estruturado**, que poderá ser revisado pelo profissional antes da exportação e do envio.

---

## Contexto do sistema
O sistema já possui:

- módulo de **pacientes**
- módulo de **avaliações**
- módulo de **testes**
- resultados por teste
- cálculo/classificação/interpretação por instrumento
- frontend em **Next.js**
- backend em **Django + API**
- arquitetura preparada para Docker

O próximo passo é criar o fluxo:

**Paciente → Avaliação → Testes preenchidos → Consolidação do contexto clínico → Geração de laudo com IA → Revisão → Exportação/Envio**

---

## Regras obrigatórias

1. **Não recalcular testes dentro do módulo de laudo**.
   - O laudo deve consumir apenas dados já salvos pela avaliação e pelos testes.

2. **A IA não deve gerar laudo a partir de texto solto**.
   - Antes da chamada ao modelo, o sistema deve montar um **contexto clínico estruturado**.

3. **O laudo gerado pela IA deve ser um rascunho editável**.
   - Nunca tratar a primeira geração como documento final.

4. **O laudo deve ser vinculado a uma avaliação**.
   - A entidade central do fluxo é a avaliação, não o teste isolado.

5. **O sistema deve permitir regeneração por seção**.
   - Ex.: regenerar apenas conclusão, hipótese diagnóstica ou atenção.

6. **O sistema deve manter versionamento básico**.
   - Preservar texto gerado originalmente, texto editado e versão final.

7. **A arquitetura deve ser modular e escalável**.
   - Implementar app próprio de laudos/reports com services bem separados.

---

## Entrega esperada
Implementar um novo módulo chamado `reports` ou `laudos`, contendo:

- models
- services
- selectors
- api
- schemas
- geração por IA
- frontend de revisão
- exportação futura preparada
- integração com avaliação e testes

---

# 1. Estrutura backend esperada

Criar um novo app Django:

```text
apps/reports/
  __init__.py
  apps.py
  admin.py
  selectors.py

  models/
    __init__.py
    reports.py
    versions.py

  services/
    __init__.py
    report_context_service.py
    report_generation_service.py
    report_section_service.py
    report_validation_service.py
    report_export_service.py
    report_delivery_service.py

  prompts/
    __init__.py
    templates.py
    rules.py
    sections.py

  api/
    __init__.py
    router.py
    schemas.py
    endpoints.py

  migrations/
    __init__.py
```

---

# 2. Modelos a serem criados

## 2.1 Report
Criar modelo principal `Report`.

Campos sugeridos:

- `id`
- `evaluation` (FK para avaliação)
- `patient` (FK para paciente)
- `status`
- `prompt_version`
- `context_payload` (JSON)
- `generated_text` (TextField)
- `edited_text` (TextField)
- `final_text` (TextField)
- `generated_sections` (JSON)
- `last_generation_metadata` (JSON)
- `created_at`
- `updated_at`
- `generated_at`
- `finalized_at`
- `created_by`
- `updated_by`

### Status sugeridos
- `draft`
- `generated`
- `reviewed`
- `finalized`
- `exported`
- `sent`

## 2.2 ReportVersion
Criar modelo simples para versionamento.

Campos sugeridos:
- `id`
- `report` (FK)
- `version_number`
- `source` (`generated`, `manual_edit`, `section_regeneration`, `final`)
- `content`
- `metadata` (JSON)
- `created_at`
- `created_by`

---

# 3. Papel de cada service

## 3.1 `report_context_service.py`
Responsável por montar o **contexto estruturado** da avaliação.

Deve consolidar:
- dados do paciente
- dados da avaliação
- anamnese
- observações clínicas
- lista de testes aplicados
- resultados estruturados de cada teste
- interpretações já disponíveis
- hipóteses diagnósticas preliminares, se existirem

### Saída esperada
Um JSON padronizado, por exemplo:

```json
{
  "patient": {
    "name": "Nome",
    "age": 12,
    "schooling": "7º ano"
  },
  "evaluation": {
    "id": 1,
    "reason": "Investigação de dificuldades atencionais"
  },
  "anamnesis": {
    "summary": "..."
  },
  "clinical_observations": {
    "summary": "..."
  },
  "tests": [
    {
      "instrument": "WISC-IV",
      "report_section": "EFICIÊNCIA INTELECTUAL",
      "structured_results": {},
      "clinical_interpretation": "..."
    }
  ]
}
```

## 3.2 `report_generation_service.py`
Responsável por:
- receber contexto estruturado
- aplicar regras de prompt
- chamar o provedor de IA
- gerar o rascunho completo
- salvar resultado no `Report`

Deve possuir métodos como:
- `generate_full_report(evaluation_id, user)`
- `regenerate_full_report(report_id, user)`

## 3.3 `report_section_service.py`
Responsável por regenerar seções específicas.

Métodos sugeridos:
- `generate_section(report_id, section_name, user)`
- `replace_section(report_id, section_name, content, user)`

Seções possíveis:
- identificacao
- descricao_demanda
- anamnese
- eficiencia_intelectual
- atencao
- funcoes_executivas
- linguagem
- gnosias_praxias
- memoria_aprendizagem
- escalas_complementares
- conclusao
- hipotese_diagnostica
- sugestoes_conduta

## 3.4 `report_validation_service.py`
Validar se a avaliação tem dados suficientes para gerar laudo.

Exemplos de validação:
- avaliação existe
- paciente vinculado existe
- há pelo menos um teste concluído
- anamnese presente ou observação indicando ausência
- resultados estruturados disponíveis

## 3.5 `report_export_service.py`
Preparar exportação futura.

Inicialmente:
- montar HTML limpo do laudo
- preparar base para DOCX/PDF

Não precisa finalizar a exportação agora, mas deixar pronto o ponto de integração.

## 3.6 `report_delivery_service.py`
Preparar envio futuro por:
- e-mail
- WhatsApp

Inicialmente pode apenas expor a interface do service e deixar TODOs claros.

---

# 4. Padronização obrigatória dos testes para uso no laudo

Cada instrumento deve poder fornecer um payload padrão para o módulo de laudos.

Criar um contrato/interface de saída para os testes.

Exemplo:

```python
{
    "instrument": "BPA-2",
    "domain": "Atenção",
    "report_section": "ATENÇÃO",
    "summary": "Desempenho inferior em atenção alternada e média inferior em atenção geral.",
    "structured_results": {...},
    "clinical_interpretation": "..."
}
```

Implementar helper genérico que percorra os testes vinculados à avaliação e normalize a saída.

Se algum teste ainda não tiver interpretação estruturada suficiente, o service deve:
- usar o que estiver disponível
- registrar warning técnico
- nunca quebrar a geração do laudo inteiro

---

# 5. Templates e prompts

Criar pasta `apps/reports/prompts/`.

## 5.1 `templates.py`
Deve conter o template base do laudo com marcadores de seção.

## 5.2 `rules.py`
Deve conter regras fixas de escrita, por exemplo:
- linguagem técnica
- coerência clínica
- evitar repetições excessivas
- respeitar nomenclaturas diagnósticas
- não inventar dados ausentes
- indicar insuficiência de dados quando necessário
- usar apenas conteúdo presente no contexto estruturado

## 5.3 `sections.py`
Prompts por seção.

Exemplo:
- prompt de conclusão
- prompt de hipótese diagnóstica
- prompt de atenção
- prompt de memória

---

# 6. Estrutura do laudo a ser gerado

A IA deve gerar o laudo nesse formato base:

1. Identificação
2. Descrição da demanda
3. Procedimentos / testes utilizados
4. Anamnese
5. Análise
   - Eficiência intelectual
   - Atenção
   - Funções executivas
   - Linguagem
   - Gnosias e praxias
   - Memória e aprendizagem
   - Escalas/instrumentos complementares
6. Conclusão
7. Hipótese diagnóstica
8. Sugestões de conduta

O texto deve ser salvo também em formato seccionado, para permitir regeneração parcial.

---

# 7. API backend esperada

Criar endpoints como:

## Geração
- `POST /api/reports/generate-from-evaluation/{evaluation_id}`
- `POST /api/reports/{report_id}/regenerate`
- `POST /api/reports/{report_id}/generate-section/{section_name}`

## Leitura
- `GET /api/reports/`
- `GET /api/reports/{report_id}`
- `GET /api/reports/by-evaluation/{evaluation_id}`

## Edição
- `PUT /api/reports/{report_id}`
- `PATCH /api/reports/{report_id}/sections/{section_name}`
- `POST /api/reports/{report_id}/finalize`

## Exportação
- `POST /api/reports/{report_id}/export-docx`
- `POST /api/reports/{report_id}/export-pdf`

## Envio
- `POST /api/reports/{report_id}/send-email`
- `POST /api/reports/{report_id}/send-whatsapp`

---

# 8. Schemas da API

Criar `schemas.py` contendo:

- `ReportListSchema`
- `ReportDetailSchema`
- `GenerateReportInputSchema`
- `GenerateSectionInputSchema`
- `UpdateReportSchema`
- `FinalizeReportSchema`
- `ReportExportSchema`
- `ReportDeliverySchema`

Campos importantes:
- `evaluation_id`
- `report_id`
- `status`
- `generated_text`
- `edited_text`
- `final_text`
- `sections`
- `metadata`

---

# 9. Fluxo funcional obrigatório

## Fluxo principal
1. Usuário acessa uma avaliação.
2. Sistema verifica testes concluídos.
3. Usuário clica em **Gerar laudo com IA**.
4. Backend valida os dados.
5. Backend consolida o contexto clínico.
6. Backend chama a IA.
7. Sistema cria o `Report` com status `generated`.
8. Frontend abre a tela de revisão.
9. Usuário edita o texto.
10. Usuário salva versão final.
11. Usuário exporta e/ou envia.

## Fluxo de regeneração por seção
1. Usuário abre laudo.
2. Clica em regenerar seção.
3. Backend usa o contexto salvo + seção desejada.
4. Atualiza apenas a seção.
5. Cria nova versão.

---

# 10. Frontend esperado

Implementar no Next.js:

```text
app/(dashboard)/reports/
  page.tsx
  [id]/page.tsx
  generate/[evaluationId]/page.tsx

components/reports/
  ReportList.tsx
  ReportEditor.tsx
  ReportSectionsSidebar.tsx
  ReportActions.tsx
  ReportStatusBadge.tsx
  GenerateReportButton.tsx
  SectionRegenerateButton.tsx
```

## 10.1 Tela de lista de laudos
- listar laudos
- status
- paciente
- avaliação
- data
- botão abrir

## 10.2 Tela de geração
- mostrar resumo da avaliação
- testes concluídos
- botão `Gerar laudo com IA`
- feedback visual de loading

## 10.3 Tela de edição/revisão
Deve conter:
- editor principal
- navegação por seções
- botão salvar
- botão regenerar seção
- botão finalizar
- botão exportar DOCX
- botão exportar PDF
- botão enviar
- histórico básico de versões

---

# 11. Comportamento esperado da IA

A IA deve:
- usar apenas dados fornecidos
- manter coerência clínica
- integrar anamnese + observação + testes
- evitar contradições
- sinalizar ausência de dados sem inventar
- gerar texto técnico revisável

A IA não deve:
- inventar resultados
- criar diagnóstico sem base mínima
- ignorar o contexto estruturado
- misturar seções

---

# 12. Estratégia técnica de implementação

Implementar em fases.

## Fase 1 — Backend base
- criar app `reports`
- model `Report`
- selectors
- schemas
- endpoints básicos

## Fase 2 — Consolidação de contexto
- montar `report_context_service.py`
- integrar dados da avaliação
- integrar testes e interpretações

## Fase 3 — Geração com IA
- criar prompt base
- criar service de geração
- salvar rascunho

## Fase 4 — Frontend de revisão
- tela de geração
- tela de edição
- salvar texto editado

## Fase 5 — Versionamento e regeneração por seção
- criar `ReportVersion`
- regeneração parcial

## Fase 6 — Exportação e envio
- DOCX/PDF
- e-mail
- WhatsApp

---

# 13. Critérios de aceitação

A implementação só será considerada pronta quando:

- for possível gerar um laudo a partir de uma avaliação
- o laudo for salvo no banco
- o usuário puder editar o texto
- o usuário puder regenerar seções específicas
- existir versionamento básico
- o fluxo não recalcular testes
- a geração depender apenas de dados consolidados
- a arquitetura permanecer modular

---

# 14. Restrições técnicas

- não quebrar a estrutura atual de testes
- não acoplar lógica de laudo dentro dos módulos de instrumentos
- não gerar laudo direto no frontend
- não chamar IA sem contexto estruturado
- não usar texto hardcoded dentro dos endpoints
- manter services separados de api

---

# 15. Resultado final esperado

Ao final, o sistema deverá permitir que o profissional:

1. abra uma avaliação já preenchida
2. clique em gerar laudo com IA
3. revise o rascunho gerado
4. ajuste o texto manualmente
5. finalize o laudo
6. exporte o documento
7. envie por e-mail ou WhatsApp

---

# 16. Instrução final para a IA da IDE

Implemente esse módulo seguindo estritamente a arquitetura existente do projeto.

Priorize:
- organização de código
- separação por responsabilidade
- reaproveitamento das interpretações já existentes
- escalabilidade para novos testes
- estabilidade do fluxo clínico

Sempre que houver dúvida entre solução rápida e solução modular, escolha a **solução modular**.

Não simplifique o fluxo removendo versionamento, contexto estruturado ou revisão humana.

O laudo deve ser tratado como uma entidade própria do sistema, derivada da avaliação, e não como um texto solto gerado em tela.
