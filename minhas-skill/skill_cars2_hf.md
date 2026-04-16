# SKILL COMPLETA — CARS2-HF PARA O SISTEMA

## 1. Objetivo da skill

Implementar o instrumento **CARS2-HF (Childhood Autism Rating Scale – Second Edition, High Functioning Version)** no sistema, permitindo:

- cadastro e edição da aplicação
- registro das observações clínicas de cada item
- marcação da pontuação de cada domínio
- cálculo automático do escore bruto total
- conversão automática para **T-escore** e **percentil**
- classificação automática da gravidade
- geração de interpretação técnica
- disponibilização do resultado para uso no laudo final

## 2. Estrutura recomendada do módulo

```text
apps/tests/
  norms/
    cars2_hf/
      raw_to_tscore.csv

  cars2_hf/
    __init__.py
    config.py
    schemas.py
    validators.py
    constants.py
    loaders.py
    calculators.py
    classifiers.py
    interpreters.py
```

## 3. Estrutura clínica do CARS2-HF

O instrumento deve conter os 15 itens abaixo, exatamente nesta ordem, pois o escore final depende da soma de todos eles:

1. Compreensão sócio-emocional  
2. Expressão emocional e regulação das emoções  
3. Relacionamento com pessoas  
4. Uso do corpo  
5. Uso de objetos nas brincadeiras  
6. Adaptação a mudanças / interesses restritos  
7. Resposta visual  
8. Resposta auditiva  
9. Resposta a, ou uso de, sabor, cheiro e toque  
10. Medo ou ansiedade  
11. Comunicação verbal  
12. Comunicação não verbal  
13. Habilidades de integração de pensamento/cognitiva  
14. Leve e consistente resposta intelectual  
15. Impressões gerais

## 4. Regras de pontuação

Cada item aceita apenas os seguintes valores:

```python
VALID_SCORES = [1, 1.5, 2, 2.5, 3, 3.5, 4]
```

### Regra geral
- `1.0` = comportamento dentro do esperado
- `1.5` = leve alteração
- `2.0` = alteração discreta
- `2.5` = alteração moderada
- `3.0` = alteração clinicamente relevante
- `3.5` = alteração severa
- `4.0` = alteração muito grave

### Escore final
O sistema deve:
1. somar os 15 itens
2. obter o `raw_total`
3. converter o total em `t_score`
4. converter o total em `percentile`
5. aplicar a classificação clínica final

## 5. Classificação clínica final

Segundo o protocolo, a classificação do escore bruto total deve seguir esta regra:

- **15 a 27,5** → Sintomas mínimos ou inexistentes do transtorno do espectro do autismo
- **28 a 33,5** → Leve a moderado sintomas do transtorno do espectro do autismo
- **Acima de 34** → Sintomas severos do transtorno do espectro do autismo

### Função de classificação

```python
def classify_severity(raw_total: float) -> str:
    if 15 <= raw_total <= 27.5:
        return "Sintomas mínimos ou inexistentes do transtorno do espectro do autismo"
    if 28 <= raw_total <= 33.5:
        return "Leve a moderado sintomas do transtorno do espectro do autismo"
    if raw_total > 34:
        return "Sintomas severos do transtorno do espectro do autismo"
    return "Resultado inválido"
```

## 6. Conversão para T-escore e percentil

O protocolo traz uma tabela normativa relacionando:

- `Escore bruto`
- `T-escore`
- `Percentil`

Como há intervalos e valores fracionados, o ideal é salvar isso em CSV.

### Arquivo `raw_to_tscore.csv`

Formato sugerido:

```csv
raw_min,raw_max,t_score,percentile
47.0,999.0,70,97+
46.5,46.5,69,97
46.0,46.0,68,96
45.5,45.5,67,96
45.0,45.0,66,95
44.0,44.5,65,93
43.5,43.5,64,92
42.5,43.0,63,90
41.5,42.0,62,88
41.0,41.0,61,86
40.5,40.5,60,84
39.5,40.0,59,82
38.5,39.0,58,79
38.0,38.0,57,76
37.5,37.5,56,72
37.0,37.0,55,69
36.0,36.5,54,65
35.5,35.5,53,62
35.0,35.0,52,58
34.0,34.5,51,54
33.0,33.5,50,50
32.5,32.5,49,46
32.0,32.0,48,42
31.5,31.5,47,38
30.5,31.0,46,33
30.0,30.0,45,31
29.5,29.5,44,28
28.5,29.0,43,24
28.0,28.0,42,21
27.5,27.5,41,19
27.0,27.0,40,16
26.5,26.5,39,14
26.0,26.0,38,12
25.0,25.5,37,10
24.5,24.5,36,8
24.0,24.0,35,7
23.5,23.5,34,6
23.0,23.0,33,5
22.0,22.5,32,4
21.5,21.5,31,3
21.0,21.0,30,2
20.5,20.5,29,1
20.0,20.0,28,1
19.5,19.5,27,<1
19.0,19.0,26,<1
18.5,18.5,25,<1
18.0,18.0,20,<1
0.0,17.999,19,<1
```

### Observação técnica

Como o protocolo apresenta faixas visuais e algumas linhas agrupadas, o CSV deve ser revisado manualmente durante a implementação final para garantir aderência perfeita à tabela normativa do PDF. A estrutura acima é a base correta de modelagem.

## 7. `constants.py`

```python
ITEMS = [
    ("compreensao_socio_emocional", "Compreensão sócio-emocional"),
    ("expressao_emocional_regulacao", "Expressão emocional e regulação das emoções"),
    ("relacionamento_com_pessoas", "Relacionamento com pessoas"),
    ("uso_do_corpo", "Uso do corpo"),
    ("uso_objetos_brincadeiras", "Uso de objetos nas brincadeiras"),
    ("adaptacao_mudancas_interesses_restritos", "Adaptação a mudanças / interesses restritos"),
    ("resposta_visual", "Resposta visual"),
    ("resposta_auditiva", "Resposta auditiva"),
    ("resposta_sensorial", "Resposta a, ou uso de, sabor, cheiro e toque"),
    ("medo_ou_ansiedade", "Medo ou ansiedade"),
    ("comunicacao_verbal", "Comunicação verbal"),
    ("comunicacao_nao_verbal", "Comunicação não verbal"),
    ("integracao_pensamento_cognicao", "Habilidades de integração de pensamento/cognitiva"),
    ("resposta_intelectual", "Leve e consistente resposta intelectual"),
    ("impressoes_gerais", "Impressões gerais"),
]

VALID_SCORES = [1, 1.5, 2, 2.5, 3, 3.5, 4]
```

## 8. `schemas.py`

Modelo esperado para `raw_payload`:

```python
from pydantic import BaseModel
from typing import Dict, Optional

class CARS2HFItemInput(BaseModel):
    score: float
    observations: Optional[str] = ""

class CARS2HFInput(BaseModel):
    patient_name: Optional[str] = None
    evaluation_date: Optional[str] = None
    examiner_name: Optional[str] = None
    birth_date: Optional[str] = None
    age_years: Optional[int] = None
    age_months: Optional[int] = None
    informant: Optional[str] = None
    items: Dict[str, CARS2HFItemInput]
```

## 9. `validators.py`

```python
from .constants import ITEMS, VALID_SCORES

def validate_cars2_hf_payload(payload: dict) -> None:
    if "items" not in payload:
        raise ValueError("O campo 'items' é obrigatório.")

    expected_keys = {key for key, _ in ITEMS}
    received_keys = set(payload["items"].keys())

    missing = expected_keys - received_keys
    extra = received_keys - expected_keys

    if missing:
        raise ValueError(f"Itens obrigatórios ausentes: {sorted(missing)}")

    if extra:
        raise ValueError(f"Itens desconhecidos enviados: {sorted(extra)}")

    for key, item in payload["items"].items():
        score = item.get("score")
        if score not in VALID_SCORES:
            raise ValueError(
                f"Pontuação inválida para '{key}'. Valores permitidos: {VALID_SCORES}"
            )
```

## 10. `loaders.py`

```python
import csv
from pathlib import Path

def load_cars2_hf_norms() -> list[dict]:
    path = Path(__file__).resolve().parent.parent / "norms" / "cars2_hf" / "raw_to_tscore.csv"
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "raw_min": float(row["raw_min"]),
                "raw_max": float(row["raw_max"]),
                "t_score": row["t_score"],
                "percentile": row["percentile"],
            })
    return rows
```

## 11. `calculators.py`

```python
from .constants import ITEMS
from .loaders import load_cars2_hf_norms

def calculate_raw_total(items: dict) -> float:
    return round(sum(float(items[key]["score"]) for key, _ in ITEMS), 1)

def convert_raw_to_norms(raw_total: float) -> dict:
    norms = load_cars2_hf_norms()
    for row in norms:
        if row["raw_min"] <= raw_total <= row["raw_max"]:
            return {
                "t_score": row["t_score"],
                "percentile": row["percentile"],
            }
    return {
        "t_score": None,
        "percentile": None,
    }

def get_highest_domains(items: dict, top_n: int = 3) -> list[str]:
    sorted_items = sorted(
        items.items(),
        key=lambda pair: pair[1]["score"],
        reverse=True
    )
    return [name for name, _ in sorted_items[:top_n]]

def build_computed_payload(payload: dict) -> dict:
    items = payload["items"]
    raw_total = calculate_raw_total(items)
    norms = convert_raw_to_norms(raw_total)

    return {
        "raw_total": raw_total,
        "t_score": norms["t_score"],
        "percentile": norms["percentile"],
        "highest_domains": get_highest_domains(items),
        "domain_scores": {
            key: items[key]["score"] for key, _ in ITEMS
        }
    }
```

## 12. `classifiers.py`

```python
def classify_cars2_hf(raw_total: float) -> dict:
    if 15 <= raw_total <= 27.5:
        return {
            "severity_group": "Sintomas mínimos ou inexistentes do transtorno do espectro do autismo",
            "severity_code": "minimal_or_none"
        }
    elif 28 <= raw_total <= 33.5:
        return {
            "severity_group": "Leve a moderado sintomas do transtorno do espectro do autismo",
            "severity_code": "mild_to_moderate"
        }
    elif raw_total > 34:
        return {
            "severity_group": "Sintomas severos do transtorno do espectro do autismo",
            "severity_code": "severe"
        }
    return {
        "severity_group": "Resultado inválido",
        "severity_code": "invalid"
    }
```

## 13. `interpreters.py`

A interpretação deve ser técnica, objetiva e compatível com laudo.

### Função base

```python
from .constants import ITEMS

LABELS = {key: label for key, label in ITEMS}

def build_cars2_hf_interpretation(computed_payload: dict, classification: dict) -> str:
    raw_total = computed_payload["raw_total"]
    t_score = computed_payload["t_score"]
    percentile = computed_payload["percentile"]
    severity_group = classification["severity_group"]

    highest = computed_payload["highest_domains"]
    highest_labels = [LABELS.get(x, x) for x in highest]

    text = (
        f"No CARS2-HF, o escore bruto total foi {raw_total}, "
        f"correspondente a T-escore {t_score} e percentil {percentile}. "
        f"Esse resultado situa o examinando na faixa de "
        f"{severity_group.lower()}. "
    )

    if highest_labels:
        text += (
            f"Os maiores indicadores de comprometimento estiveram presentes em "
            f"{', '.join(highest_labels[:-1]) + ' e ' + highest_labels[-1] if len(highest_labels) > 1 else highest_labels[0]}, "
            f"sugerindo maior impacto relativo nesses domínios."
        )

    return text
```

## 14. Modelo de interpretação clínica mais refinado

Você pode usar este modelo fixo:

```text
O CARS2-HF evidenciou escore bruto total de {raw_total}, correspondente a T-escore {t_score} e percentil {percentile}. A classificação obtida situa o examinando na faixa de {severity_group_lower}. Observa-se que os indicadores mais elevados concentraram-se nos domínios de {highest_domains_text}, sugerindo maior comprometimento relativo em aspectos associados à reciprocidade social, comunicação e flexibilidade comportamental, conforme o perfil individual apresentado no protocolo.
```

### Regra adicional para laudo
- se `severity_code = minimal_or_none`: usar linguagem cautelosa
- se `severity_code = mild_to_moderate`: usar linguagem de indicativos compatíveis
- se `severity_code = severe`: usar linguagem de comprometimento importante

## 15. `config.py`

```python
from .validators import validate_cars2_hf_payload
from .calculators import build_computed_payload
from .classifiers import classify_cars2_hf
from .interpreters import build_cars2_hf_interpretation

class CARS2HFModule:
    code = "CARS2_HF"
    name = "CARS2 – HF"

    def validate(self, raw_payload: dict) -> None:
        validate_cars2_hf_payload(raw_payload)

    def score(self, raw_payload: dict) -> dict:
        computed = build_computed_payload(raw_payload)
        classification = classify_cars2_hf(computed["raw_total"])
        interpretation = build_cars2_hf_interpretation(computed, classification)

        return {
            "computed_payload": {
                **computed,
                **classification,
            },
            "interpretation": interpretation,
        }
```

## 16. Registro no `registry.py`

```python
from apps.tests.cars2_hf.config import CARS2HFModule

TEST_REGISTRY = {
    "CARS2_HF": CARS2HFModule(),
}
```

## 17. Estrutura do `raw_payload`

Exemplo realista:

```json
{
  "patient_name": "Paciente Exemplo",
  "evaluation_date": "2026-04-15",
  "examiner_name": "André",
  "birth_date": "2016-02-10",
  "age_years": 10,
  "age_months": 2,
  "informant": "Mãe",
  "items": {
    "compreensao_socio_emocional": { "score": 2.5, "observations": "Dificuldade para compreender nuances emocionais." },
    "expressao_emocional_regulacao": { "score": 2.0, "observations": "Oscilações emocionais e rigidez em situações frustrantes." },
    "relacionamento_com_pessoas": { "score": 3.0, "observations": "Baixa reciprocidade social." },
    "uso_do_corpo": { "score": 1.5, "observations": "Sem estereotipias evidentes; leve rigidez motora." },
    "uso_objetos_brincadeiras": { "score": 2.5, "observations": "Brincadeira simbólica restrita." },
    "adaptacao_mudancas_interesses_restritos": { "score": 3.0, "observations": "Resistência importante a mudanças." },
    "resposta_visual": { "score": 2.5, "observations": "Contato visual inconsistente." },
    "resposta_auditiva": { "score": 1.5, "observations": "Responde ao nome, mas de forma irregular." },
    "resposta_sensorial": { "score": 2.0, "observations": "Sensibilidade seletiva a texturas." },
    "medo_ou_ansiedade": { "score": 2.0, "observations": "Ansiedade em situações novas." },
    "comunicacao_verbal": { "score": 2.5, "observations": "Discurso pouco recíproco." },
    "comunicacao_nao_verbal": { "score": 3.0, "observations": "Gestos pouco integrados à comunicação." },
    "integracao_pensamento_cognicao": { "score": 2.0, "observations": "Dificuldade em integrar informações globais." },
    "resposta_intelectual": { "score": 1.5, "observations": "Funcionamento cognitivo global preservado, com discrepâncias." },
    "impressoes_gerais": { "score": 3.0, "observations": "Conjunto clínico compatível com alterações do espectro autista." }
  }
}
```

## 18. Estrutura do `computed_payload`

```json
{
  "raw_total": 34.0,
  "t_score": 51,
  "percentile": 54,
  "severity_group": "Sintomas severos do transtorno do espectro do autismo",
  "severity_code": "severe",
  "highest_domains": [
    "relacionamento_com_pessoas",
    "adaptacao_mudancas_interesses_restritos",
    "comunicacao_nao_verbal"
  ],
  "domain_scores": {
    "compreensao_socio_emocional": 2.5,
    "expressao_emocional_regulacao": 2.0,
    "relacionamento_com_pessoas": 3.0,
    "uso_do_corpo": 1.5,
    "uso_objetos_brincadeiras": 2.5,
    "adaptacao_mudancas_interesses_restritos": 3.0,
    "resposta_visual": 2.5,
    "resposta_auditiva": 1.5,
    "resposta_sensorial": 2.0,
    "medo_ou_ansiedade": 2.0,
    "comunicacao_verbal": 2.5,
    "comunicacao_nao_verbal": 3.0,
    "integracao_pensamento_cognicao": 2.0,
    "resposta_intelectual": 1.5,
    "impressoes_gerais": 3.0
  }
}
```

## 19. Layout ideal no frontend

### Cabeçalho
- Nome
- Data da avaliação
- Data de nascimento
- Idade
- Informante
- Avaliador

### Corpo principal
15 cards verticais, cada um com:
- título do item
- resumo curto do critério
- seletor da pontuação
- textarea de observações

### Seletor de pontuação
```text
1 | 1.5 | 2 | 2.5 | 3 | 3.5 | 4
```

### Rodapé automático
- escore bruto total
- T-escore
- percentil
- classificação final

## 20. Comportamento do frontend

### Regras
- exibir cálculo em tempo real
- atualizar classificação sem reload
- marcar itens obrigatórios
- impedir salvar com item faltando
- destacar automaticamente os três domínios mais elevados no resumo final

### UX recomendada
- cards com borda discreta
- pontuação em botões segmentados
- observações sempre abaixo do seletor
- resumo final em card fixo ao final da página

## 21. Integração com laudo

Na geração do laudo, o CARS2-HF deve expor:
- escore bruto total
- T-escore
- percentil
- classificação
- interpretação técnica
- principais domínios alterados

### Campo ideal no `result_summary`

```json
{
  "test_name": "CARS2 – HF",
  "raw_total": 34.0,
  "t_score": 51,
  "percentile": 54,
  "severity_group": "Sintomas severos do transtorno do espectro do autismo",
  "interpretation": "O CARS2-HF evidenciou..."
}
```

## 22. Observação clínica importante para o sistema

O próprio protocolo do CARS2-HF indica relação com **alto funcionamento** e menciona no item 14 a expectativa de uso em indivíduos com **QI acima de 80**. Então o sistema pode trazer um aviso como:

> “Este protocolo é destinado à versão de alto funcionamento. Verificar compatibilidade com o perfil cognitivo do examinando.”

Isso não precisa bloquear o uso, mas deve aparecer como orientação clínica.

## 23. Prompt interno para a IA da IDE

Use este prompt no seu gerador:

```text
Implementar o teste CARS2-HF no app apps/tests seguindo a arquitetura modular já usada no sistema.

Criar a pasta apps/tests/cars2_hf/ com os arquivos:
- __init__.py
- config.py
- schemas.py
- validators.py
- constants.py
- loaders.py
- calculators.py
- classifiers.py
- interpreters.py

Criar também a pasta de normas:
apps/tests/norms/cars2_hf/raw_to_tscore.csv

Requisitos:
1. O teste possui 15 itens obrigatórios.
2. Cada item aceita apenas os valores: 1, 1.5, 2, 2.5, 3, 3.5, 4.
3. O sistema deve validar todos os itens antes do cálculo.
4. O escore bruto total é a soma dos 15 itens.
5. O escore bruto total deve ser convertido em T-escore e percentil usando o CSV.
6. A classificação clínica final deve seguir:
   - 15 a 27.5 = sintomas mínimos ou inexistentes
   - 28 a 33.5 = leve a moderado
   - acima de 34 = severos
7. O módulo deve retornar computed_payload + interpretation.
8. A interpretação deve mencionar:
   - escore bruto
   - T-escore
   - percentil
   - classificação
   - domínios mais elevados
9. Registrar o módulo em apps/tests/registry.py com o código CARS2_HF.
10. O código deve ser limpo, tipado e pronto para integração com Django.
```

## 24. Resultado esperado

Ao final da implementação, o sistema deverá:
- permitir responder todo o protocolo
- calcular automaticamente o total
- retornar conversão normativa
- indicar gravidade clínica
- gerar interpretação automática pronta para ser aproveitada no laudo

## 25. Fechamento

Essa skill já está pronta como base de implementação real para o seu sistema.

O próximo passo técnico natural é gerar os arquivos reais do módulo:
- `constants.py`
- `schemas.py`
- `validators.py`
- `loaders.py`
- `calculators.py`
- `classifiers.py`
- `interpreters.py`
- `config.py`
- `raw_to_tscore.csv`

Assim você já cola direto no projeto.
