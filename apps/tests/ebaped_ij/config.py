from enum import Enum
from dataclasses import dataclass

EBADEPIJ_CODE = "ebaped_ij"
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
    1: "Item 01",
    2: "Item 02",
    3: "Item 03",
    4: "Item 04",
    5: "Item 05",
    6: "Item 06",
    7: "Item 07",
    8: "Item 08",
    9: "Item 09",
    10: "Item 10",
    11: "Item 11",
    12: "Item 12",
    13: "Item 13",
    14: "Item 14",
    15: "Item 15",
    16: "Item 16",
    17: "Item 17",
    18: "Item 18",
    19: "Item 19",
    20: "Item 20",
    21: "Item 21",
    22: "Item 22",
    23: "Item 23",
    24: "Item 24",
    25: "Item 25",
    26: "Item 26",
    27: "Item 27",
}

RESPONSE_LABELS = {
    0: "Nunca/Poucas vezes",
    1: "Algumas vezes",
    2: "Muitas vezes/Sempre",
}
