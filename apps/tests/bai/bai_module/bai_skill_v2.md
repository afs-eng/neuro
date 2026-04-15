# SKILL — Implementação do teste BAI no sistema Django

## Objetivo
Implementar o teste **BAI — Beck Anxiety Inventory** no sistema, seguindo a arquitetura modular dos instrumentos já existentes, com suporte a:

- cadastro e validação das 21 respostas
- cálculo automático do escore bruto
- classificação da intensidade da ansiedade
- geração de tabelas estruturadas para frontend e laudo
- geração de gráficos
- interpretação técnica inicial
- integração com o registro central de testes
- saída padronizada em `raw_payload`, `computed_payload` e `interpretation_payload`

## Diretrizes obrigatórias

1. A implementação deve seguir o padrão modular do app `apps/tests/`.
2. O teste deve funcionar tanto para exibição em tela quanto para composição de laudo.
3. O sistema deve separar claramente:
   - dados inseridos pelo usuário
   - resultados calculados
   - blocos interpretativos
4. O escore bruto deve ser sempre calculado pela soma dos 21 itens.
5. A classificação clínica deve ser determinada por faixa normativa configurável.
6. A implementação deve permitir evolução futura para norma por escore T, percentil e intervalo de confiança.
7. Os gráficos devem ser gerados em Python, com saída utilizável no sistema.
8. O código deve ser organizado para manutenção simples e expansão futura.

## Estrutura de pastas esperada

```text
apps/tests/
  __init__.py
  registry.py

  services/
    __init__.py
    scoring_service.py
    interpretation_service.py

  norms/
    __init__.py
    bai/
      classification.csv
      t_score_lookup.csv

  bai/
    __init__.py
    config.py
    schemas.py
    validators.py
    constants.py
    loaders.py
    calculators.py
    classifiers.py
    interpreters.py
    presenters.py
    charts.py
```

## Responsabilidade de cada arquivo

### `apps/tests/bai/config.py`
Arquivo principal do módulo.
Deve expor a classe `BAIModule`, responsável por conectar:

- schema de entrada
- validação
- cálculo
- classificação
- interpretação
- apresentação dos dados finais

Exemplo de responsabilidade:

```python
class BAIModule:
    code = "BAI"
    name = "Inventário de Ansiedade de Beck"
```

### `apps/tests/bai/schemas.py`
Define o formato dos dados aceitos pelo teste.
Usar `pydantic`, `dataclass` ou schema equivalente já utilizado no sistema.

Deve conter:

- estrutura de respostas dos 21 itens
- campos auxiliares opcionais
- metadados de aplicação

### `apps/tests/bai/validators.py`
Valida o payload recebido.

Regras mínimas:

- todos os 21 itens devem existir
- cada item deve aceitar somente valores válidos
- não permitir respostas fora da escala
- impedir valores nulos quando o teste for finalizado

### `apps/tests/bai/constants.py`
Centraliza constantes fixas.

Deve conter:

- lista oficial dos 21 itens
- legenda das respostas
- nomes dos blocos de saída
- faixas padrão de classificação
- rótulos dos gráficos

### `apps/tests/bai/loaders.py`
Responsável por carregar tabelas normativas e faixas auxiliares a partir de CSV.

Deve prever:

- leitura de `classification.csv`
- leitura futura de `t_score_lookup.csv`

### `apps/tests/bai/calculators.py`
Executa os cálculos principais.

Deve:

- somar o escore bruto
- contar frequências de resposta
- calcular percentuais de distribuição das respostas
- preparar dados numéricos para gráficos

### `apps/tests/bai/classifiers.py`
Transforma os resultados numéricos em classificação clínica.

Deve:

- receber o escore bruto
- consultar a tabela de classificação
- retornar faixa normativa e descrição clínica

### `apps/tests/bai/interpreters.py`
Gera texto interpretativo técnico inicial.

Deve produzir:

- um resumo clínico breve
- descrição da intensidade da ansiedade
- observação sobre o padrão de respostas
- texto neutro, técnico e revisável

### `apps/tests/bai/presenters.py`
Monta a saída final para frontend e laudo.

Deve devolver:

- tabela principal do teste
- tabela dos itens
- tabela de estatísticas das respostas
- dados estruturados para renderização de gráficos

### `apps/tests/bai/charts.py`
Gera os gráficos do teste.

Deve suportar:

- gráfico de perfil do escore total
- curva com posicionamento do valor
- gráfico de distribuição das respostas

## Modelo de dados do teste

## Escala de resposta
Cada item deve aceitar apenas um inteiro entre `0` e `3`.

Mapeamento:

- `0` = Absolutamente não
- `1` = Levemente: Não me incomodou muito
- `2` = Moderadamente: Foi muito desagradável, mas pude suportar
- `3` = Gravemente: Dificilmente pude suportar

## Itens do BAI
A implementação deve usar os 21 itens abaixo:

```python
BAI_ITEMS = [
    (1, "Dormência ou formigamento"),
    (2, "Sensação de calor"),
    (3, "Tremores nas pernas"),
    (4, "Incapaz de relaxar"),
    (5, "Medo que aconteça o pior"),
    (6, "Atordoado ou tonto"),
    (7, "Palpitação ou aceleração do coração"),
    (8, "Sem equilíbrio"),
    (9, "Aterrorizado"),
    (10, "Nervoso"),
    (11, "Sensação de sufocação"),
    (12, "Tremores nas mãos"),
    (13, "Trêmulo"),
    (14, "Medo de perder o controle"),
    (15, "Dificuldade de respirar"),
    (16, "Medo de morrer"),
    (17, "Assustado"),
    (18, "Indigestão ou desconforto no abdômen"),
    (19, "Sensação de desmaio"),
    (20, "Rosto afogueado"),
    (21, "Suor (não devido ao calor)"),
]
```

## Estrutura de `raw_payload`

Formato esperado:

```json
{
  "application_mode": "manual",
  "responses": {
    "1": 0,
    "2": 2,
    "3": 1,
    "4": 3,
    "5": 2,
    "6": 1,
    "7": 2,
    "8": 0,
    "9": 1,
    "10": 3,
    "11": 1,
    "12": 0,
    "13": 1,
    "14": 2,
    "15": 1,
    "16": 0,
    "17": 2,
    "18": 1,
    "19": 0,
    "20": 1,
    "21": 2
  },
  "notes": "campo opcional"
}
```

## Estrutura de `computed_payload`

Formato esperado:

```json
{
  "instrument": "BAI",
  "total_raw_score": 26,
  "classification": {
    "label": "Moderado",
    "description": "Nível moderado de ansiedade"
  },
  "response_statistics": {
    "count_0": 4,
    "count_1": 7,
    "count_2": 6,
    "count_3": 4,
    "percent_0": 19.05,
    "percent_1": 33.33,
    "percent_2": 28.57,
    "percent_3": 19.05
  },
  "table_summary": [
    {
      "scale": "Escore Total",
      "raw_score": 26,
      "norm_value": "Moderado"
    }
  ],
  "item_analysis": [
    {
      "item": 1,
      "label": "Dormência ou formigamento",
      "response_value": 0,
      "response_label": "Absolutamente não",
      "points": 0
    }
  ],
  "chart_payload": {
    "profile": {},
    "distribution": {},
    "bell_curve": {}
  }
}
```

## Estrutura de `interpretation_payload`

Formato esperado:

```json
{
  "summary": "Os resultados do BAI indicam nível moderado de ansiedade, com presença clinicamente relevante de sintomas ansiosos autorreferidos.",
  "clinical_interpretation": "A distribuição das respostas sugere frequência importante de sintomas fisiológicos e cognitivos compatíveis com ansiedade de intensidade moderada.",
  "technical_note": "O BAI é um instrumento de autorrelato e seus resultados devem ser interpretados em conjunto com os dados clínicos, observacionais e demais instrumentos aplicados."
}
```

## Regras de cálculo

### Escore bruto total
O escore bruto total deve ser a soma simples dos 21 itens.

Fórmula:

```python
total_raw_score = sum(responses.values())
```

Faixa possível:

- mínimo: `0`
- máximo: `63`

### Estatísticas das respostas
O sistema deve calcular:

- quantidade de respostas 0
- quantidade de respostas 1
- quantidade de respostas 2
- quantidade de respostas 3
- percentual de cada categoria

### Tabela de classificação
Criar inicialmente a tabela abaixo em `classification.csv`.
Essa tabela deve ser lida pelo módulo, e não ficar hardcoded no classificador.

```csv
min_score,max_score,label,description
0,10,Mínimo,Nível mínimo de ansiedade
11,19,Leve,Nível brando de ansiedade
20,30,Moderado,Nível moderado de ansiedade
31,63,Grave,Nível severo de ansiedade
```

## Regras de classificação

### Lógica
1. Receber `total_raw_score`
2. Buscar a faixa correspondente no CSV
3. Retornar:
   - `label`
   - `description`
   - intervalo usado

### Exemplo
- `0 a 10` → Mínimo
- `11 a 19` → Leve
- `20 a 30` → Moderado
- `31 a 63` → Grave

## Tabelas que o módulo deve gerar

### 1. Tabela principal de escores
Formato:

```json
[
  {
    "scale": "Escore Total",
    "raw_score": 35,
    "norm_value": "Moderado",
    "description": "Nível moderado de ansiedade"
  }
]
```

### 2. Tabela de análise dos itens
Cada linha deve conter:

- número do item
- nome abreviado ou nome completo
- resposta numérica
- resposta textual
- pontuação

### 3. Tabela de estatísticas das respostas
Cada linha deve conter:

- categoria de resposta
- quantidade
- percentual

Exemplo:

```json
[
  {"response": 0, "label": "Absolutamente não", "count": 2, "percent": 9.52},
  {"response": 1, "label": "Levemente", "count": 8, "percent": 38.10},
  {"response": 2, "label": "Moderadamente", "count": 6, "percent": 28.57},
  {"response": 3, "label": "Gravemente", "count": 5, "percent": 23.81}
]
```

## Gráficos que devem ser implementados

### 1. Gráfico de perfil do escore total
Objetivo:
Mostrar visualmente a posição do escore bruto dentro do intervalo total do BAI.

Sugestão:
- eixo horizontal de 0 a 63
- marcador do escore do paciente
- faixas clínicas ao fundo

### 2. Curva de posicionamento do escore
Objetivo:
Gerar um gráfico em forma de curva para destacar o posicionamento do escore observado.

Observação:
Na versão inicial, pode usar apenas uma curva ilustrativa padronizada. Quando a tabela normativa completa estiver disponível, substituir por posicionamento normativo real.

### 3. Gráfico de distribuição das respostas
Objetivo:
Mostrar a frequência das respostas 0, 1, 2 e 3.

Sugestão:
- gráfico de barras horizontal ou vertical
- exibir quantidade e percentual

## Interface esperada para o frontend
O módulo deve retornar dados prontos para a tela do teste, contemplando:

- card com escore bruto total
- card com classificação
- tabela de escores
- tabela detalhada dos itens
- gráfico de perfil
- gráfico de distribuição
- bloco interpretativo

## Integração com o `registry.py`
Registrar o instrumento no registro central.

Exemplo:

```python
from apps.tests.bai.config import BAIModule

TEST_REGISTRY = {
    "BAI": BAIModule(),
}
```

## Integração com `scoring_service.py`
Fluxo esperado:

1. receber `instrument_code = "BAI"`
2. localizar o módulo no registry
3. validar `raw_payload`
4. calcular resultados
5. classificar escore
6. montar `computed_payload`
7. gerar `interpretation_payload`
8. devolver tudo consolidado

## Contrato do módulo
A classe `BAIModule` deve expor algo equivalente a:

```python
class BAIModule:
    code = "BAI"
    name = "Inventário de Ansiedade de Beck"

    def validate(self, raw_payload):
        ...

    def score(self, raw_payload):
        ...

    def interpret(self, computed_payload):
        ...

    def present(self, computed_payload, interpretation_payload):
        ...
```

## Requisitos técnicos do código

1. Usar Python com tipagem sempre que possível.
2. Separar cálculo, classificação e interpretação.
3. Evitar regras clínicas hardcoded fora de `constants.py` e CSVs.
4. Preferir funções puras para cálculo.
5. Garantir facilidade de teste unitário.
6. Permitir futura inclusão de:
   - escore T
   - percentil
   - intervalo de confiança
   - comparação com normas por sexo, idade ou amostra

## Exemplo de implementação mínima da classificação

```python
from dataclasses import dataclass
import pandas as pd

@dataclass
class ClassificationResult:
    label: str
    description: str
    min_score: int
    max_score: int


def classify_bai(total_raw_score: int, classification_df: pd.DataFrame) -> ClassificationResult:
    row = classification_df[
        (classification_df["min_score"] <= total_raw_score)
        & (classification_df["max_score"] >= total_raw_score)
    ].iloc[0]

    return ClassificationResult(
        label=row["label"],
        description=row["description"],
        min_score=int(row["min_score"]),
        max_score=int(row["max_score"]),
    )
```

## Exemplo de interpretação inicial

A IA deve gerar um texto com estrutura parecida com esta:

> Os resultados obtidos no Inventário de Ansiedade de Beck indicam intensidade [mínima/leve/moderada/grave] de sintomas ansiosos autorreferidos. O escore bruto total sugere presença de manifestações compatíveis com ansiedade em grau [descrição clínica], com distribuição de respostas que evidencia [predomínio leve/moderado/importante] de sintomas ao longo dos itens investigados. Por se tratar de um instrumento de autorrelato, a interpretação deve ser realizada em conjunto com a entrevista clínica, observações comportamentais e demais instrumentos utilizados no processo avaliativo.

## Prompt operacional para a IA implementar
Use este comando como instrução de execução:

```text
Implemente o instrumento BAI no app apps/tests/ do sistema Django, seguindo a arquitetura modular já existente para testes. Crie os arquivos apps/tests/bai/config.py, schemas.py, validators.py, constants.py, loaders.py, calculators.py, classifiers.py, interpreters.py, presenters.py e charts.py, além da pasta apps/tests/norms/bai/ com classification.csv e estrutura preparada para t_score_lookup.csv.

O módulo deve receber raw_payload com 21 respostas de 0 a 3, calcular o escore bruto total, classificar por faixa normativa usando CSV, montar computed_payload com tabela principal, análise item a item, estatísticas de resposta e dados para gráficos, e gerar interpretation_payload com texto técnico inicial.

Integre o módulo ao registry.py e o deixe compatível com o scoring_service.py. Escreva código limpo, tipado, escalável e pronto para evolução futura.
```

## Prompt operacional para a IA gerar a interface

```text
Crie a interface frontend do teste BAI de forma profissional e limpa. A tela deve permitir registrar os 21 itens com respostas de 0 a 3, exibir legenda da escala, mostrar card com escore total, card com classificação clínica, tabela dos itens, tabela de estatísticas das respostas e gráficos de perfil e distribuição. O layout deve ser responsivo e visualmente consistente com os demais testes do sistema.
```

## Entrega esperada
Ao final, a IA deve entregar:

1. todos os arquivos Python do módulo BAI
2. arquivo CSV de classificação
3. funções de cálculo e classificação prontas
4. interpretador técnico inicial
5. dados de gráficos prontos para renderização
6. integração no registro central de instrumentos
7. código preparado para uso em Django

