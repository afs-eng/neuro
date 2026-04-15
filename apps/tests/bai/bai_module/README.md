# Módulo BAI em Python para o sistema

Estrutura sugerida:

```text
apps/tests/
  bai/
    __init__.py
    config.py
    schemas.py
    validators.py
    calculators.py
    classifiers.py
    interpreters.py
    charts.py
    constants.py
  norms/
    bai/
      README.md
```

## O que este módulo entrega

- validação dos 21 itens do BAI
- cálculo do escore bruto total
- classificação por faixa normativa
- estimativa inicial de escore T, percentil e intervalo de confiança
- tabelas prontas para UI e laudo
- geração de gráficos em PNG para uso no frontend, PDF ou DOCX
- texto interpretativo técnico inicial

## Integração rápida

No `registry.py`:

```python
from apps.tests.bai import BAIModule

TEST_REGISTRY = {
    "BAI": BAIModule(chart_output_dir="/tmp/test_charts/bai"),
}
```

No serviço:

```python
module = TEST_REGISTRY["BAI"]
computed_payload = module.run(raw_payload)
```

## Formato esperado do raw_payload

```python
{
  "respondent_name": "Paciente",
  "application_mode": "paper",
  "responses": [
    {"item_number": 1, "score": 0},
    {"item_number": 2, "score": 1},
    ...,
    {"item_number": 21, "score": 2}
  ]
}
```

## Observação importante

O exemplo usa uma conversão estimada de escore bruto para escore T/percentil para deixar o módulo funcional já no início.
Quando você cadastrar a tabela normativa oficial do BAI no sistema, basta substituir:

- `estimate_t_score`
- `estimate_percentile`
- `estimate_confidence_interval`

por leitura de CSV ou lookup em banco.
