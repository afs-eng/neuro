# SKILL — Módulo Laudo

## Objetivo
Implementar no sistema um módulo de Laudo Neuropsicológico robusto, modular, revisável e compatível com geração final em `.docx`, seguindo o modelo clínico do profissional e separando:
- estrutura fixa do documento;
- dados objetivos vindos da avaliação;
- interpretação clínica assistida por IA;
- revisão humana;
- exportação final.

## Princípios do módulo
1. O laudo não deve ser gerado em um único bloco de texto solto.
2. O laudo deve ser composto por seções independentes.
3. A IA deve escrever apenas as partes clínicas interpretativas.
4. Resultados objetivos, tabelas, identificações e metadados devem vir do sistema.
5. O profissional deve poder revisar cada seção antes da finalização.
6. O `.docx` final deve ser montado pelo backend.

## Estrutura geral do módulo
O módulo de Laudo deve funcionar como um motor de composição documental clínica.

Fluxo esperado:
1. usuário abre uma avaliação concluída;
2. sistema identifica o paciente e os testes preenchidos;
3. sistema monta um contexto clínico estruturado;
4. sistema cria um rascunho de laudo;
5. IA gera as seções clínicas;
6. usuário revisa;
7. backend gera o `.docx` final.

## Tipos de template
O sistema deve suportar, no mínimo:
- laudo infantil
- laudo adolescente
- laudo adulto

Cada template define:
- ordem das seções;
- cabeçalhos;
- blocos fixos;
- textos institucionais;
- assinatura;
- referências padrão.

## Estrutura do laudo por seções
As seções devem ser modeladas separadamente.

Seções principais:
- Identificação
- Descrição da Demanda
- Procedimentos
- Anamnese / História Clínica
- Eficiência Intelectual
- Atenção
- Funções Executivas
- Linguagem
- Gnosias e Praxias
- Memória e Aprendizagem
- RAVLT
- FDT
- E-TDAH-PAIS
- E-TDAH-AD
- SCARED
- SRS-2
- EPQ-J
- BAI
- EBADEP
- BFP / IPHEXA
- Conclusão
- Hipótese Diagnóstica
- Sugestões de Conduta
- Considerações Finais
- Referências

A exibição deve ser condicional: apenas seções compatíveis com os testes aplicados devem aparecer.

## Regras de composição
### Partes fixas
Devem vir do template, sem IA:
- título do laudo;
- subtítulo institucional;
- estrutura de cabeçalhos;
- bloco legal;
- assinatura;
- observações éticas;
- referências padrão.

### Partes variáveis objetivas
Devem vir do banco:
- nome;
- data de nascimento;
- idade;
- escolaridade;
- escola;
- filiação;
- encaminhante;
- finalidade;
- testes realizados;
- escores;
- percentis;
- classificações;
- data do documento;
- CID-11.

### Partes clínicas interpretativas
Devem ser geradas com IA:
- motivo do encaminhamento;
- síntese da anamnese;
- interpretação por domínio;
- integração entre testes;
- conclusão geral;
- hipótese diagnóstica;
- encaminhamentos.

## Banco de dados — models principais
### Report
Campos:
- id
- patient_id
- evaluation_id
- template_type
- status
- title
- version
- created_by
- updated_by
- created_at
- updated_at
- finalized_at

### ReportSection
Campos:
- id
- report_id
- section_key
- section_title
- section_order
- is_enabled
- is_ai_generated
- is_user_edited
- content_raw
- content_final
- created_at
- updated_at

### ReportTemplate
Campos:
- id
- name
- template_type
- description
- is_active
- header_text
- footer_text
- default_sections_json
- legal_text
- signature_block
- references_default
- created_at
- updated_at

### ReportTestRule
Campos:
- id
- test_code
- domain_key
- intro_template
- interpretation_rules_json
- closing_template
- supports_table
- supports_chart
- created_at
- updated_at

### ReportPreference
Campos:
- id
- user_id
- use_first_name_only
- include_hypothesis_section
- use_dsm_5_tr
- use_cid_11
- include_tables
- include_charts
- default_template_type
- conclusion_style
- use_em_analise_clinica
- avoid_long_dashes
- created_at
- updated_at

## Serviços de backend
### ReportContextService
Responsável por montar o contexto clínico estruturado do laudo.

Funções:
- carregar dados do paciente;
- carregar dados da avaliação;
- identificar testes aplicados;
- carregar resultados;
- carregar observações clínicas;
- aplicar preferências do profissional;
- gerar JSON final para IA.

### ReportBuilderService
Responsável pela composição do laudo.

Funções:
- criar rascunho;
- criar seções padrão;
- preencher seções fixas;
- chamar IA para seções clínicas;
- montar conclusão;
- salvar versões.

### ReportAIService
Responsável apenas pela redação clínica.

Funções:
- gerar anamnese resumida;
- gerar interpretação por teste;
- gerar integração clínica;
- gerar conclusão;
- gerar hipótese diagnóstica;
- gerar encaminhamentos.

A IA não deve:
- inventar escore;
- inventar percentil;
- recalcular teste;
- alterar dados cadastrais;
- criar seção não aplicada;
- fechar diagnóstico sem base.

### ReportDocxService
Responsável por montar o `.docx`.

Funções:
- abrir template `.docx`;
- inserir seções;
- inserir tabelas;
- inserir gráficos;
- aplicar formatação;
- exportar arquivo final.

### ReportChartService
Responsável por gerar gráficos como imagem.

Exemplos:
- gráfico WISC-IV / WASI
- gráfico BPA-2
- gráfico RAVLT
- gráfico FDT
- gráfico SRS-2
- radar de personalidade

## Fluxo ideal do usuário
1. Abrir avaliação do paciente.
2. Clicar em “Gerar Laudo”.
3. Sistema verifica se há dados suficientes.
4. Sistema cria rascunho.
5. Sistema preenche identificação e procedimentos.
6. IA gera as seções clínicas.
7. Usuário revisa cada bloco.
8. Usuário aprova.
9. Sistema gera `.docx`.
10. Sistema salva versão final.

## Estados do laudo
Sugestão:
- draft
- generated
- under_review
- reviewed
- finalized
- archived

## Editor do laudo
O editor deve ser por seções, não por texto único.

Layout sugerido:
### Coluna esquerda
- lista das seções

### Área central
- editor da seção selecionada

### Coluna direita
- dados do paciente
- resultados dos testes
- observações clínicas
- ações da IA
- botão “Regenerar seção”

## JSON padrão para IA
A IA deve receber um JSON estruturado, não texto solto.

Exemplo mínimo:
```json
{
  "report_meta": {
    "template_type": "adolescente",
    "city": "Goiânia",
    "report_date": "2026-04-07"
  },
  "patient": {
    "full_name": "Nome completo",
    "preferred_name": "Primeiro nome",
    "sex": "Feminino",
    "birth_date": "2011-04-24",
    "age_text": "14 anos e 8 meses",
    "schooling": "8º ano do ensino fundamental"
  },
  "referral": {
    "interested_party": "Familiares",
    "purpose": "Averiguação das capacidades cognitivas para auxílio diagnóstico",
    "chief_complaint": "..."
  },
  "anamnese": {
    "pregnancy": "...",
    "birth": "...",
    "development": "...",
    "sleep": "...",
    "feeding": "...",
    "school_history": "...",
    "routine": "...",
    "medical_history": "..."
  },
  "tests_applied": [],
  "test_results": {},
  "observations": {
    "session_behavior": "...",
    "clinical_notes": "..."
  },
  "preferences": {
    "use_first_name_only": true,
    "include_hypothesis_section": true,
    "use_dsm_5_tr": true,
    "use_cid_11": true,
    "include_tables": true,
    "include_charts": true
  }
}
```

## Regras por teste
Cada teste deve ter:
- introdução fixa;
- regras de interpretação;
- frases por faixa/classificação;
- fechamento clínico padrão;
- suporte opcional a tabela;
- suporte opcional a gráfico.

Isso evita que a IA escreva tudo do zero.

## Geração por seção
A geração deve ser modular.

### Sem IA
- Identificação
- Procedimentos
- lista de testes
- assinatura
- parte legal
- data/local
- referências padrão

### Com IA
- Descrição da Demanda
- Anamnese
- Eficiência Intelectual
- Atenção
- Funções Executivas
- Linguagem
- Gnosias e Praxias
- Memória e Aprendizagem
- escalas clínicas
- Conclusão
- Hipótese Diagnóstica
- Encaminhamentos

## Conclusão geral
A conclusão não deve ser mera repetição das seções anteriores.

Ela deve integrar:
- anamnese;
- observação clínica;
- resultados dos testes;
- impacto funcional;
- funcionamento escolar/social;
- hipótese diagnóstica.

A conclusão deve ser gerada por IA apenas após todas as demais seções estarem prontas.

## Hipótese diagnóstica
Deve ser uma seção própria ou um bloco ao final da conclusão, conforme preferência do profissional.

Regras:
- usar a expressão “há hipótese diagnóstica de...” quando aplicável;
- usar DSM-5-TR™ quando houver menção diagnóstica;
- incluir CID-11 se configurado;
- nunca afirmar hipótese sem base suficiente.

## Encaminhamentos
Devem ser coerentes com o caso e com a faixa etária.

Podem incluir:
- neuropediatra
- neurologista
- psiquiatra
- psicoterapia
- psicopedagogia
- terapia ocupacional
- fonoaudiologia
- orientação familiar
- adaptação escolar

## DOCX final
O `.docx` deve ser montado pelo backend.

### Texto
Inserir usando seções já revisadas.

### Tabelas
Devem ser nativas do Word, criadas pelo backend.

### Gráficos
Devem ser gerados em imagem e inseridos no documento.

A IA não deve montar manualmente tabelas ou gráficos no documento.

## Estrutura de pastas sugerida
```python
apps/
  reports/
    models.py
    schemas.py
    selectors.py
    api.py
    services/
      report_context.py
      report_builder.py
      report_ai.py
      report_docx.py
      report_chart.py
    templates/
      docx/
        laudo_base_infantil.docx
        laudo_base_adolescente.docx
        laudo_base_adulto.docx
    prompts/
      report_section_prompts.py
      report_conclusion_prompts.py
```

## Endpoints sugeridos
- `POST /reports/create-from-evaluation/{evaluation_id}`
- `GET /reports/{report_id}`
- `GET /reports/{report_id}/sections`
- `POST /reports/{report_id}/generate-section/{section_key}`
- `POST /reports/{report_id}/generate-all`
- `PATCH /reports/{report_id}/sections/{section_id}`
- `POST /reports/{report_id}/finalize`
- `GET /reports/{report_id}/export-docx`

## Ordem recomendada de implementação
### Fase 1
- models
- CRUD básico do laudo
- editor por seções

### Fase 2
- leitura automática da avaliação
- preenchimento automático da identificação e procedimentos

### Fase 3
- contexto clínico estruturado
- JSON padronizado para IA

### Fase 4
- geração por seção com IA

### Fase 5
- revisão manual
- versionamento

### Fase 6
- DOCX com tabelas e gráficos

## Regra final
O módulo Laudo deve ser:
- modular;
- confiável;
- revisável;
- centrado em dados estruturados;
- fiel ao estilo clínico do profissional;
- escalável para múltiplos modelos de laudo.
