from __future__ import annotations

# 21 itens oficiais do BAI (Beck Anxiety Inventory)
ITEMS = [
    "Dormência ou formigamento",
    "Sensação de calor",
    "Tremores nas pernas",
    "Incapaz de relaxar",
    "Medo que aconteça o pior",
    "Atordoado ou tonto",
    "Palpitação ou aceleração do coração",
    "Sem equilíbrio",
    "Aterrorizado",
    "Nervoso",
    "Sensação de sufocação",
    "Tremores nas mãos",
    "Trêmulo",
    "Medo de perder o controle",
    "Dificuldade de respirar",
    "Medo de morrer",
    "Assustado",
    "Indigestão ou desconforto no abdômen",
    "Sensação de desmaio",
    "Rosto afogueado",
    "Suor (não devido ao calor)",
]

RESPONSE_OPTIONS = {
    0: "Absolutamente não",
    1: "Levemente: Não me incomodou muito",
    2: "Moderadamente: Foi muito desagradável, mas pude suportar",
    3: "Gravemente: Dificilmente pude suportar",
}

RESPONSE_OPTIONS_SHORT = {
    0: "Absolutamente não",
    1: "Levemente",
    2: "Moderadamente",
    3: "Gravemente",
}

RESPONSE_OPTIONS_WITH_CODE = {
    score: f"({score + 1}) {label}" for score, label in RESPONSE_OPTIONS_SHORT.items()
}

# Faixas normativas do escore bruto do BAI (Beck et al., 1988)
RAW_SCORE_BANDS = [
    {
        "key": "minimo",
        "label": "Mínimo",
        "min": 0,
        "max": 10,
        "interpretation": "Nível mínimo de ansiedade",
    },
    {
        "key": "leve",
        "label": "Leve",
        "min": 11,
        "max": 19,
        "interpretation": "Nível brando de ansiedade",
    },
    {
        "key": "moderado",
        "label": "Moderado",
        "min": 20,
        "max": 30,
        "interpretation": "Nível moderado de ansiedade",
    },
    {
        "key": "grave",
        "label": "Grave",
        "min": 31,
        "max": 63,
        "interpretation": "Nível severo de ansiedade",
    },
]

# Escore T aproximado por faixas clínicas (pode ser substituído por tabela oficial)
T_SCORE_BANDS = [
    {"key": "minimo", "label": "Mínimo", "min": 20, "max": 54},
    {"key": "leve", "label": "Leve", "min": 55, "max": 64},
    {"key": "moderado", "label": "Moderado", "min": 65, "max": 74},
    {"key": "grave", "label": "Grave", "min": 75, "max": 80},
]
