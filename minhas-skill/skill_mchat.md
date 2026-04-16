# SKILL COMPLETA — M-CHAT PARA O SISTEMA

## 1. Objetivo da skill

Implementar o **M-CHAT (Modified Checklist for Autism in Toddlers)** no sistema como instrumento de **triagem precoce para sinais de autismo**, permitindo:

- cadastro da aplicação
- preenchimento das 23 questões
- marcação de respostas `Sim` / `Não`
- conversão automática das respostas em **passa/falha**
- cálculo do total de falhas
- identificação automática das falhas em **itens críticos**
- classificação do resultado de triagem
- geração de interpretação técnica breve
- disponibilização do resultado para o laudo e para o prontuário

## 2. Base clínica do instrumento

O M-CHAT é um instrumento de rastreamento precoce do autismo, aplicado a **pais ou cuidadores**, voltado para crianças de **18 a 24 meses**. É uma escala simples, autoaplicável, composta por **23 questões dicotômicas (Sim/Não)**. A literatura brasileira de tradução destaca seu uso como ferramenta de triagem, e não de diagnóstico definitivo.

## 3. Estrutura recomendada do módulo

```text
apps/tests/
  norms/
    mchat/
      scoring_rules.json

  mchat/
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

## 4. Estrutura clínica do M-CHAT

O instrumento contém **23 itens**, todos obrigatórios:

1. Seu filho gosta de se balançar, de pular no seu joelho, etc.?
2. Seu filho tem interesse por outras crianças?
3. Seu filho gosta de subir em coisas, como escadas ou móveis?
4. Seu filho gosta de brincar de esconder e mostrar o rosto ou de esconde-esconde?
5. Seu filho já brincou de faz-de-conta, como, por exemplo, fazer de conta que está falando no telefone ou que está cuidando da boneca, ou qualquer outra brincadeira de faz-de-conta?
6. Seu filho já usou o dedo indicador dele para apontar, para pedir alguma coisa?
7. Seu filho já usou o dedo indicador dele para apontar, para indicar interesse em algo?
8. Seu filho consegue brincar de forma correta com brinquedos pequenos (ex. carros ou blocos), sem apenas colocar na boca, remexer no brinquedo ou deixar o brinquedo cair?
9. O seu filho alguma vez trouxe objetos para você (pais) para lhe mostrar este objeto?
10. O seu filho olha para você no olho por mais de um segundo ou dois?
11. O seu filho já pareceu muito sensível ao barulho (ex. tapando os ouvidos)?
12. O seu filho sorri em resposta ao seu rosto ou ao seu sorriso?
13. O seu filho imita você? (ex. você faz expressões/caretas e seu filho imita?)
14. O seu filho responde quando você chama ele pelo nome?
15. Se você aponta um brinquedo do outro lado do cômodo, o seu filho olha para ele?
16. Seu filho já sabe andar?
17. O seu filho olha para coisas que você está olhando?
18. O seu filho faz movimentos estranhos com os dedos perto do rosto dele?
19. O seu filho tenta atrair a sua atenção para a atividade dele?
20. Você alguma vez já se perguntou se seu filho é surdo?
21. O seu filho entende o que as pessoas dizem?
22. O seu filho às vezes fica aéreo, “olhando para o nada” ou caminhando sem direção definida?
23. O seu filho olha para o seu rosto para conferir a sua reação quando vê algo estranho?

## 5. Regra de cotação

As respostas `Sim/Não` não são interpretadas diretamente como acerto ou erro. Elas devem ser convertidas em **passa/falha** conforme a chave de cotação.

Segundo o protocolo, o resultado é considerado alterado quando houver:

- **falha em 3 itens ou mais no total**
- **ou falha em 2 itens críticos**

Os **itens críticos** são:

- 2
- 7
- 9
- 13
- 14
- 15

## 6. Chave de falha por item

As respostas consideradas **Falha** são:

| Item | Resposta que indica falha |
|------|----------------------------|
| 1 | Não |
| 2 | Não |
| 3 | Não |
| 4 | Não |
| 5 | Não |
| 6 | Não |
| 7 | Não |
| 8 | Não |
| 9 | Não |
| 10 | Não |
| 11 | Sim |
| 12 | Não |
| 13 | Não |
| 14 | Não |
| 15 | Não |
| 16 | Não |
| 17 | Não |
| 18 | Sim |
| 19 | Não |
| 20 | Sim |
| 21 | Não |
| 22 | Sim |
| 23 | Não |

## 7. `constants.py`

```python
ITEMS = [
    (1, "gosta_de_balancar"),
    (2, "interesse_outras_criancas"),
    (3, "gosta_de_subir"),
    (4, "brinca_esconder_mostrar"),
    (5, "brinca_faz_de_conta"),
    (6, "aponta_para_pedir"),
    (7, "aponta_para_mostrar_interesse"),
    (8, "brinca_corretamente_com_objetos"),
    (9, "traz_objetos_para_mostrar"),
    (10, "contato_visual"),
    (11, "hipersensibilidade_a_ruido"),
    (12, "sorri_em_resposta"),
    (13, "imita_o_adulto"),
    (14, "responde_ao_nome"),
    (15, "segue_apontar"),
    (16, "ja_sabe_andar"),
    (17, "olha_para_o_que_o_adulto_olha"),
    (18, "movimentos_estranhos_dedos_rosto"),
    (19, "busca_atencao_para_atividade"),
    (20, "suspeita_de_surdez"),
    (21, "entende_o_que_dizem"),
    (22, "fica_aereo_ou_deambula"),
    (23, "checa_reacao_facial"),
]

VALID_RESPONSES = ["Sim", "Não"]

CRITICAL_ITEMS = {2, 7, 9, 13, 14, 15}

FAILURE_RULES = {
    1: "Não",
    2: "Não",
    3: "Não",
    4: "Não",
    5: "Não",
    6: "Não",
    7: "Não",
    8: "Não",
    9: "Não",
    10: "Não",
    11: "Sim",
    12: "Não",
    13: "Não",
    14: "Não",
    15: "Não",
    16: "Não",
    17: "Não",
    18: "Sim",
    19: "Não",
    20: "Sim",
    21: "Não",
    22: "Sim",
    23: "Não",
}
```

## 8. `schemas.py`

```python
from pydantic import BaseModel
from typing import Dict, Optional

class MCHATResponseItem(BaseModel):
    answer: str

class MCHATInput(BaseModel):
    patient_name: Optional[str] = None
    evaluation_date: Optional[str] = None
    birth_date: Optional[str] = None
    age_months: Optional[int] = None
    respondent_name: Optional[str] = None
    respondent_relationship: Optional[str] = None
    items: Dict[str, MCHATResponseItem]
```

## 9. `validators.py`

```python
from .constants import ITEMS, VALID_RESPONSES

def validate_mchat_payload(payload: dict) -> None:
    if "items" not in payload:
        raise ValueError("O campo 'items' é obrigatório.")

    expected_keys = {slug for _, slug in ITEMS}
    received_keys = set(payload["items"].keys())

    missing = expected_keys - received_keys
    extra = received_keys - expected_keys

    if missing:
        raise ValueError(f"Itens obrigatórios ausentes: {sorted(missing)}")

    if extra:
        raise ValueError(f"Itens desconhecidos enviados: {sorted(extra)}")

    for key, item in payload["items"].items():
        answer = item.get("answer")
        if answer not in VALID_RESPONSES:
            raise ValueError(
                f"Resposta inválida para '{key}'. Valores permitidos: {VALID_RESPONSES}"
            )
```

## 10. `loaders.py`

Como a lógica do M-CHAT é fixa, você pode optar por não usar CSV. Ainda assim, para manter padrão modular, pode salvar as regras em JSON.

### `scoring_rules.json`

```json
{
  "critical_items": [2, 7, 9, 13, 14, 15],
  "failure_rules": {
    "1": "Não",
    "2": "Não",
    "3": "Não",
    "4": "Não",
    "5": "Não",
    "6": "Não",
    "7": "Não",
    "8": "Não",
    "9": "Não",
    "10": "Não",
    "11": "Sim",
    "12": "Não",
    "13": "Não",
    "14": "Não",
    "15": "Não",
    "16": "Não",
    "17": "Não",
    "18": "Sim",
    "19": "Não",
    "20": "Sim",
    "21": "Não",
    "22": "Sim",
    "23": "Não"
  }
}
```

## 11. `calculators.py`

```python
from .constants import ITEMS, FAILURE_RULES, CRITICAL_ITEMS

ITEM_NUMBER_BY_SLUG = {slug: number for number, slug in ITEMS}

def is_failure(item_number: int, answer: str) -> bool:
    return FAILURE_RULES[item_number] == answer

def build_computed_payload(payload: dict) -> dict:
    item_results = {}
    total_failures = 0
    critical_failures = 0
    failed_items = []
    failed_critical_items = []

    for item_number, slug in ITEMS:
        answer = payload["items"][slug]["answer"]
        failed = is_failure(item_number, answer)

        item_results[slug] = {
            "item_number": item_number,
            "answer": answer,
            "result": "Falha" if failed else "Passa",
            "is_critical": item_number in CRITICAL_ITEMS,
        }

        if failed:
            total_failures += 1
            failed_items.append(item_number)

            if item_number in CRITICAL_ITEMS:
                critical_failures += 1
                failed_critical_items.append(item_number)

    return {
        "total_failures": total_failures,
        "critical_failures": critical_failures,
        "failed_items": failed_items,
        "failed_critical_items": failed_critical_items,
        "item_results": item_results,
    }
```

## 12. `classifiers.py`

```python
def classify_mchat(computed_payload: dict) -> dict:
    total_failures = computed_payload["total_failures"]
    critical_failures = computed_payload["critical_failures"]

    if total_failures >= 3 or critical_failures >= 2:
        return {
            "screen_result": "Triagem positiva para risco de sinais compatíveis com TEA",
            "screen_code": "positive"
        }

    return {
        "screen_result": "Triagem negativa no M-CHAT",
        "screen_code": "negative"
    }
```

## 13. `interpreters.py`

```python
def build_mchat_interpretation(computed_payload: dict, classification: dict) -> str:
    total_failures = computed_payload["total_failures"]
    critical_failures = computed_payload["critical_failures"]
    failed_items = computed_payload["failed_items"]
    failed_critical_items = computed_payload["failed_critical_items"]
    screen_result = classification["screen_result"]

    text = (
        f"No M-CHAT, observou-se {total_failures} falha(s) no total, "
        f"sendo {critical_failures} em item(ns) crítico(s). "
        f"O resultado indica {screen_result.lower()}."
    )

    if failed_items:
        text += f" Os itens com falha foram: {', '.join(str(i) for i in failed_items)}."

    if failed_critical_items:
        text += (
            f" Entre os itens críticos, houve falha em: "
            f"{', '.join(str(i) for i in failed_critical_items)}."
        )

    if classification["screen_code"] == "positive":
        text += (
            " Trata-se de instrumento de rastreamento, de modo que um resultado positivo "
            "sugere necessidade de investigação clínica mais aprofundada."
        )

    return text
```

## 14. Modelo de interpretação clínica mais refinado

```text
No M-CHAT, foram identificadas {total_failures} falhas no total, incluindo {critical_failures} falhas em itens críticos. Considerando os critérios de triagem do instrumento, o resultado foi classificado como {screen_result_lower}. Trata-se de instrumento de rastreamento precoce, não diagnóstico, sendo recomendado aprofundamento clínico sempre que o protocolo indicar risco aumentado.
```

## 15. `config.py`

```python
from .validators import validate_mchat_payload
from .calculators import build_computed_payload
from .classifiers import classify_mchat
from .interpreters import build_mchat_interpretation

class MCHATModule:
    code = "MCHAT"
    name = "M-CHAT"

    def validate(self, raw_payload: dict) -> None:
        validate_mchat_payload(raw_payload)

    def score(self, raw_payload: dict) -> dict:
        computed = build_computed_payload(raw_payload)
        classification = classify_mchat(computed)
        interpretation = build_mchat_interpretation(computed, classification)

        return {
            "computed_payload": {
                **computed,
                **classification
            },
            "interpretation": interpretation,
        }
```

## 16. Registro no `registry.py`

```python
from apps.tests.mchat.config import MCHATModule

TEST_REGISTRY = {
    "MCHAT": MCHATModule(),
}
```

## 17. Estrutura do `raw_payload`

```json
{
  "patient_name": "Paciente Exemplo",
  "evaluation_date": "2026-04-15",
  "birth_date": "2024-02-10",
  "age_months": 22,
  "respondent_name": "Mãe",
  "respondent_relationship": "Mãe",
  "items": {
    "gosta_de_balancar": {"answer": "Sim"},
    "interesse_outras_criancas": {"answer": "Não"},
    "gosta_de_subir": {"answer": "Sim"},
    "brinca_esconder_mostrar": {"answer": "Sim"},
    "brinca_faz_de_conta": {"answer": "Não"},
    "aponta_para_pedir": {"answer": "Sim"},
    "aponta_para_mostrar_interesse": {"answer": "Não"},
    "brinca_corretamente_com_objetos": {"answer": "Sim"},
    "traz_objetos_para_mostrar": {"answer": "Não"},
    "contato_visual": {"answer": "Sim"},
    "hipersensibilidade_a_ruido": {"answer": "Não"},
    "sorri_em_resposta": {"answer": "Sim"},
    "imita_o_adulto": {"answer": "Não"},
    "responde_ao_nome": {"answer": "Não"},
    "segue_apontar": {"answer": "Não"},
    "ja_sabe_andar": {"answer": "Sim"},
    "olha_para_o_que_o_adulto_olha": {"answer": "Sim"},
    "movimentos_estranhos_dedos_rosto": {"answer": "Não"},
    "busca_atencao_para_atividade": {"answer": "Sim"},
    "suspeita_de_surdez": {"answer": "Não"},
    "entende_o_que_dizem": {"answer": "Sim"},
    "fica_aereo_ou_deambula": {"answer": "Não"},
    "checa_reacao_facial": {"answer": "Sim"}
  }
}
```

## 18. Estrutura do `computed_payload`

```json
{
  "total_failures": 7,
  "critical_failures": 5,
  "failed_items": [2, 5, 7, 9, 13, 14, 15],
  "failed_critical_items": [2, 7, 9, 13, 14, 15],
  "screen_result": "Triagem positiva para risco de sinais compatíveis com TEA",
  "screen_code": "positive",
  "item_results": {
    "interesse_outras_criancas": {
      "item_number": 2,
      "answer": "Não",
      "result": "Falha",
      "is_critical": true
    }
  }
}
```

## 19. Layout ideal no frontend

### Cabeçalho
- Nome
- Data
- Data de nascimento
- Idade em meses
- Preenchido por
- Parentesco do informante

### Corpo principal
- lista com os 23 itens
- cada item com:
  - número
  - enunciado
  - radio buttons `Sim` / `Não`

### Rodapé automático
- total de falhas
- falhas em itens críticos
- resultado da triagem

## 20. Regras de UX

- impedir salvamento com item em branco
- mostrar legenda:
  - `Passa`
  - `Falha`
  - `Item crítico`
- cálculo em tempo real
- destacar falhas em vermelho suave
- destacar itens críticos com marcador visual discreto
- resumo final automático após a última resposta

## 21. Integração com laudo

Na geração do laudo, o M-CHAT deve expor:
- idade da criança em meses
- total de falhas
- quantidade de falhas em itens críticos
- lista de itens alterados
- resultado da triagem
- interpretação automática

### Campo ideal no `result_summary`

```json
{
  "test_name": "M-CHAT",
  "total_failures": 7,
  "critical_failures": 5,
  "screen_result": "Triagem positiva para risco de sinais compatíveis com TEA",
  "interpretation": "No M-CHAT, observou-se..."
}
```

## 22. Regra clínica importante

O M-CHAT é um **instrumento de rastreamento**, não de diagnóstico. O sistema deve deixar isso visível no resultado final.

Mensagem sugerida:

> “Resultado de triagem. Um resultado positivo no M-CHAT indica necessidade de avaliação clínica mais aprofundada, não confirmando diagnóstico isoladamente.”

## 23. Prompt interno para a IA da IDE

```text
Implementar o teste M-CHAT no app apps/tests seguindo a arquitetura modular já usada no sistema.

Criar a pasta apps/tests/mchat/ com os arquivos:
- __init__.py
- config.py
- schemas.py
- validators.py
- constants.py
- loaders.py
- calculators.py
- classifiers.py
- interpreters.py

Criar também a pasta:
apps/tests/norms/mchat/scoring_rules.json

Requisitos:
1. O teste possui 23 itens obrigatórios.
2. Cada item aceita apenas as respostas "Sim" ou "Não".
3. O sistema deve converter respostas em passa/falha conforme a chave do M-CHAT.
4. O sistema deve calcular:
   - total de falhas
   - falhas em itens críticos
   - lista de itens com falha
5. Itens críticos: 2, 7, 9, 13, 14, 15.
6. Triagem positiva quando:
   - houver 3 ou mais falhas no total
   - ou 2 ou mais falhas em itens críticos
7. O módulo deve retornar computed_payload + interpretation.
8. A interpretação deve mencionar:
   - total de falhas
   - falhas críticas
   - itens alterados
   - resultado da triagem
9. Registrar o módulo em apps/tests/registry.py com o código MCHAT.
10. O código deve ser limpo, tipado e pronto para integração com Django.
```

## 24. Resultado esperado

Ao final da implementação, o sistema deverá:
- permitir responder todo o protocolo M-CHAT
- identificar automaticamente passa/falha por item
- calcular total e itens críticos
- gerar interpretação curta e objetiva
- disponibilizar resultado para laudo e prontuário

## 25. Fechamento

Essa skill já está pronta como base de implementação real do M-CHAT no sistema.

O próximo passo técnico natural é gerar os arquivos reais do módulo:
- `constants.py`
- `schemas.py`
- `validators.py`
- `loaders.py`
- `calculators.py`
- `classifiers.py`
- `interpreters.py`
- `config.py`
- `scoring_rules.json`

Assim você já cola direto no projeto.
