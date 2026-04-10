# Implementação do Laudo com IA

## Objetivo

Implementar no sistema um módulo de **Laudo com IA** capaz de utilizar o **contexto estruturado da avaliação neuropsicológica** para gerar um **rascunho revisável**, por seções, mantendo previsibilidade clínica, rastreabilidade e possibilidade de edição humana antes da exportação final.

A IA não deve ser responsável pelo laudo final de forma autônoma. Ela deve gerar um **primeiro rascunho técnico**, com base apenas nos dados já existentes e estruturados no sistema.

## Princípio central

O sistema não deve enviar para a IA telas, HTML, texto solto ou dados crus do banco de forma desorganizada.

O fluxo correto é:

**dados da avaliação -> contexto clínico estruturado -> geração de rascunho por seções -> revisão humana -> exportação final**

## Regra de arquitetura

O módulo de laudo deve ser separado do módulo de testes.

Os testes continuam sendo responsáveis por:

- validação dos dados
- cálculo dos escores
- classificação
- interpretação técnica específica do instrumento

O módulo de laudo será responsável por:

- consolidar os dados da avaliação
- construir o contexto clínico estruturado
- chamar a IA
- gerar seções do laudo
- armazenar rascunhos
- permitir revisão e edição
- compilar o documento final
- exportar em `.docx`

## Estrutura sugerida

```text
apps/reports/
  __init__.py
  apps.py
  admin.py

  models/
    __init__.py
    report.py
    report_section.py
    report_generation_log.py

  services/
    __init__.py
    context_builder.py
    section_generator.py
    draft_generator.py
    consistency_checker.py
    report_compiler.py
    export_service.py

  prompts/
    __init__.py
    base.py
    child_report.py
    adolescent_report.py
    adult_report.py

  api/
    __init__.py
    router.py
    schemas.py
    endpoints.py

  migrations/
    __init__.py
```

## Relação com o módulo de testes

O sistema já possui uma base correta para isso, com separação entre cálculo, classificação e interpretação por instrumento, usando serviços e módulos específicos por teste, além de um registro global para orquestração. Essa organização é a base ideal para o laudo com IA, pois o módulo de laudo poderá consumir resultados já padronizados dos instrumentos, em vez de reprocessar regras clínicas dentro da camada de IA. fileciteturn1file0

## Fonte única de verdade

O laudo deve usar apenas os dados aprovados da avaliação, vindos de:

- paciente
- avaliação
- anamnese
- observações clínicas
- testes aplicados
- resultados calculados (`computed_payload`)
- interpretações já geradas pelos módulos dos testes

A IA nunca deve recalcular teste.
A IA nunca deve classificar percentil.
A IA nunca deve inventar resultado ausente.

## Contexto estruturado da avaliação

Antes da geração do laudo, o sistema deve montar um objeto consolidado.

Exemplo:

```json
{
  "patient": {
    "name": "Maria Eduarda",
    "age": 11,
    "sex": "feminino",
    "schooling": "5º ano"
  },
  "referral": {
    "reason": "retraimento social, hipersensibilidade auditiva e dificuldades atencionais"
  },
  "anamnesis": {
    "clinical_summary": "Resumo estruturado da anamnese...",
    "development_history": "Marco do desenvolvimento...",
    "main_complaints": [
      "desatenção",
      "seletividade alimentar",
      "alteração do sono"
    ]
  },
  "clinical_observations": "Observações comportamentais em sessão...",
  "tests": [
    {
      "instrument": "WISC-IV",
      "status": "corrected",
      "computed_payload": {},
      "interpretation": "Texto interpretativo pronto"
    },
    {
      "instrument": "BPA-2",
      "status": "corrected",
      "computed_payload": {},
      "interpretation": "Texto interpretativo pronto"
    }
  ],
  "report_model": "adolescente_v1",
  "style_rules": {
    "use_first_name_only": true,
    "must_include_diagnostic_hypothesis": true,
    "clinical_style": "tecnico_objetivo"
  }
}
```

## Serviço: context_builder.py

Esse serviço será o coração do recurso.

Responsabilidades:

- buscar a avaliação
- buscar dados do paciente
- buscar anamnese
- buscar observações clínicas
- buscar testes aplicados
- buscar resultados calculados
- buscar interpretações dos testes
- organizar tudo em um schema único e previsível

Exemplo conceitual:

```python
class EvaluationContextBuilder:
    def build(self, evaluation_id: int) -> dict:
        evaluation = ...
        patient = ...
        anamnesis = ...
        tests = ...

        return {
            "patient": {...},
            "referral": {...},
            "anamnesis": {...},
            "clinical_observations": "...",
            "tests": [...],
            "report_model": "adulto_v1",
            "style_rules": {...}
        }
```

## Geração por seções

O laudo não deve ser gerado em um único bloco grande.

Deve ser gerado por seções independentes.

Seções sugeridas:

- Identificação
- Descrição da Demanda
- Anamnese
- Análise Clínica
- Eficiência Intelectual
- Atenção
- Funções Executivas
- Linguagem
- Gnosias e Praxias
- Memória e Aprendizagem
- Escalas complementares
- Conclusão
- Hipótese Diagnóstica
- Sugestões de Conduta

## Vantagens da geração por seções

- mais controle clínico
- menor risco de alucinação
- permite regerar apenas uma parte
- facilita revisão humana
- facilita auditoria
- permite reaproveitar modelos fixos

## Classificação das seções

### 1. Seções fixas
Exemplo:

- cabeçalho
- identificação
- estrutura institucional

### 2. Seções semi-fixas
Usam template com variáveis.

Exemplo:

```python
template = """
{nome} foi encaminhado(a) para avaliação neuropsicológica em razão de {motivo}.
Foram utilizados os seguintes instrumentos: {lista_testes}.
"""
```

### 3. Seções geradas por IA
Exemplo:

- conclusão integrada
- hipótese diagnóstica
- síntese clínica
- correlação entre anamnese, observação e resultados dos testes

A IA deve ser usada principalmente onde houver **integração clínica**.

## Modelos de dados sugeridos

### report.py

```python
from django.db import models

class Report(models.Model):
    evaluation = models.OneToOneField("evaluations.Evaluation", on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default="draft")
    model_key = models.CharField(max_length=100)
    generated_context = models.JSONField(default=dict)
    compiled_text = models.TextField(blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### report_section.py

```python
from django.db import models

class ReportSection(models.Model):
    report = models.ForeignKey("reports.Report", related_name="sections", on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    generated_text = models.TextField(blank=True)
    edited_text = models.TextField(blank=True)
    source_payload = models.JSONField(default=dict)
    generation_status = models.CharField(max_length=30, default="pending")
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### report_generation_log.py

```python
from django.db import models

class ReportGenerationLog(models.Model):
    report = models.ForeignKey("reports.Report", on_delete=models.CASCADE)
    section_key = models.CharField(max_length=100)
    prompt_name = models.CharField(max_length=100)
    input_payload = models.JSONField(default=dict)
    output_text = models.TextField(blank=True)
    status = models.CharField(max_length=30, default="success")
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

## Serviços principais

### context_builder.py
Monta o contexto consolidado da avaliação.

### section_generator.py
Gera uma seção específica com base em:

- nome da seção
- contexto da avaliação
- prompt do modelo

### draft_generator.py
Gera todas as seções definidas para o modelo de laudo.

### consistency_checker.py
Valida coerência entre:

- testes citados
- classificações informadas
- idade do paciente
- sexo do paciente
- hipótese diagnóstica
- resultados disponíveis

### report_compiler.py
Junta as seções na ordem correta para exibição e exportação.

### export_service.py
Gera `.docx` e futuramente `.pdf`.

## Prompts

Criar prompts separados por tipo de laudo:

- `child_report.py`
- `adolescent_report.py`
- `adult_report.py`

Também criar um prompt base com regras gerais.

### Exemplo de prompt base

```text
Você é responsável por redigir uma seção de laudo neuropsicológico.

Use exclusivamente os dados fornecidos.
Não invente sintomas, testes, classificações ou diagnósticos.
Não cite instrumentos que não estejam presentes no contexto.
Mantenha linguagem técnica, objetiva e clínica.
Siga o modelo institucional.
Quando houver indícios clínicos consistentes, utilize a expressão "hipótese diagnóstica".

Dados da avaliação:
{evaluation_context_json}
```

## Regras obrigatórias da IA

- nunca inventar resultado de teste
- nunca inventar diagnóstico fechado
- nunca trocar nome do paciente
- nunca citar instrumento ausente
- nunca contradizer `computed_payload`
- nunca ignorar restrições de estilo do sistema
- sempre respeitar o modelo do laudo
- sempre permitir revisão humana posterior

## Fluxo completo de geração

1. Usuário preenche anamnese
2. Usuário vincula testes
3. Usuário corrige os testes
4. Cada teste salva `raw_payload`, `computed_payload` e `interpretation`
5. Usuário entra na aba Laudo
6. Sistema chama `context_builder`
7. Sistema cria ou atualiza `Report`
8. Sistema gera as seções com `section_generator` ou `draft_generator`
9. Sistema salva cada seção como `ReportSection`
10. Usuário revisa e edita
11. Sistema compila versão final
12. Usuário aprova
13. Sistema exporta `.docx`

## API sugerida

```text
POST   /api/reports/{evaluation_id}/generate-draft
POST   /api/reports/{report_id}/generate-section/{section_key}
GET    /api/reports/{report_id}
PATCH  /api/reports/{report_id}/sections/{section_key}
POST   /api/reports/{report_id}/approve
POST   /api/reports/{report_id}/export-docx
```

## Schemas sugeridos

### generate-draft request

```json
{
  "model_key": "adolescente_v1",
  "regenerate_existing": true
}
```

### update section request

```json
{
  "edited_text": "Texto revisado pelo profissional"
}
```

## Frontend - aba Laudo

### Bloco 1: resumo da avaliação

Exibir:

- nome do paciente
- idade
- escolaridade
- motivo do encaminhamento
- lista de testes aplicados
- status dos testes

### Bloco 2: ações

Botões:

- Gerar rascunho
- Regerar seção
- Atualizar contexto
- Aprovar laudo
- Exportar `.docx`

### Bloco 3: editor por seções

Usar tabs ou accordion com:

- título da seção
- texto gerado
- área editável
- botão salvar
- botão restaurar original

### Bloco 4: pré-visualização final

Exibir laudo compilado antes da exportação.

## Estratégia de implementação em fases

### Fase 1
Implementar apenas:

- contexto estruturado
- geração de rascunho
- seções principais:
  - Descrição da Demanda
  - Anamnese
  - Conclusão
  - Hipótese Diagnóstica
  - Sugestões de Conduta

### Fase 2
Adicionar seções por domínio cognitivo:

- Atenção
- Memória
- Linguagem
- Funções Executivas
- Gnosias e Praxias
- Escalas complementares

### Fase 3
Adicionar exportação avançada:

- `.docx` com formatação do modelo real
- tabelas
- gráficos
- paginação
- cabeçalho e rodapé

## Benefícios dessa arquitetura

- escalável
- auditável
- segura
- previsível
- revisável
- compatível com modelos fixos de laudo
- desacoplada dos instrumentos específicos
- facilita manutenção futura

## Regra final de produto

A IA não substitui o profissional.
Ela acelera a produção do laudo por meio de um rascunho técnico estruturado, sempre revisável.

## Resumo executivo

Implementar o recurso de Laudo com IA criando:

- um `context_builder` para consolidar a avaliação
- um módulo `reports` separado do módulo de testes
- geração por seções
- persistência de rascunhos e versões editadas
- verificação de consistência
- interface de revisão
- exportação final em `.docx`

Esse é o modelo mais limpo, escalável e seguro para o seu sistema.
