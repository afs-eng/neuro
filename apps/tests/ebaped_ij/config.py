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
    1: "Sinto-me estranho e não sei por quê",
    2: "Sinto vontade de ficar longe das pessoas da minha casa",
    3: "Sinto vontade de ficar longe dos meus amigos",
    4: "Estou mais agressivo",
    5: "Sinto-me culpado",
    6: "Viver está sendo difícil para mim",
    7: "Choro",
    8: "Sinto-me triste",
    9: "Tenho vontade de fazer as coisas que gosto",
    10: "Sinto-me sozinho",
    11: "Prefiro estar só",
    12: "Acredito em um futuro bom",
    13: "Meus dias têm sido bons",
    14: "Tenho planos para o futuro",
    15: "Tenho dormido bem",
    16: "Acredito nas minhas capacidades",
    17: "Estou feliz com minha vida",
    18: "Consigo me concentrar nas minhas tarefas",
    19: "Gosto de mim como eu sou",
    20: "Tenho me sentido mal, sem estar doente",
    21: "Penso em me machucar de propósito",
    22: "Penso em me matar",
    23: "Tenho comido normalmente",
    24: "Sinto-me sem energia",
    25: "Sou esperto",
    26: "Sinto-me feio",
    27: "Sinto que as pessoas não querem estar comigo",
}

RESPONSE_LABELS = {
    0: "Nunca/Poucas vezes",
    1: "Algumas vezes",
    2: "Muitas vezes/Sempre",
}
