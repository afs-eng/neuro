from enum import Enum
from dataclasses import dataclass

EBADEPIJ_CODE = "ebadep_ij"
EBADEPIJ_NAME = (
    "EBADEP-IJ - Escala de Avaliação de Padrões de Desenvolvimento Infantil/Juvenil"
)
EBADEPIJ_VERSION = "1"

TOTAL_ITEMS = 27
MAX_SCORE_PER_ITEM = 2
MAX_SCORE_TOTAL = 54

ITENS_NEGATIVOS = {1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 20, 21, 22, 24, 26, 27}

ITENS_POSITIVOS = {9, 12, 13, 14, 15, 16, 17, 18, 19, 23, 25}

ITEM_LABELS = {
    1: "Humor deprimido",
    2: "Perda ou diminuição de prazer",
    3: "Choro",
    4: "Desesperança",
    5: "Desamparo",
    6: "Indecisão",
    7: "Sentimento de incapacidade",
    8: "Sentimentos de inadequação",
    9: "Inutilidade",
    10: "Carência/dependência",
    11: "Negativismo",
    12: "Esquiva de situações sociais",
    13: "Queda de rendimento na escola",
    14: "Autocrítica exacerbada",
    15: "Culpa",
    16: "Diminuição de concentração",
    17: "Pensamento de morte",
    18: "Autoestima rebaixada",
    19: "Falta de perspectiva sobre o presente",
    20: "Falta de perspectiva sobre o futuro (desesperança)",
    21: "Alteração de apetite",
    22: "Alteração de peso",
    23: "Insônia/hipersonia",
    24: "Lentidão/agitação psicomotora",
    25: "Fadiga/perda de energia",
    26: "Sintomas físicos (ex.: dores)",
    27: "Irritação",
}

RESPONSE_LABELS = {
    0: "Nunca/Poucas vezes",
    1: "Algumas vezes",
    2: "Muitas vezes/Sempre",
}
