from .config import WISC4_SUBTESTS, WISC4_INDICES, IndexCode


CONVERSION_TABLE: dict[str, dict[int, tuple[int, int]]] = {
    "semelhancas": {
        0: (1, 1),
        5: (5, 5),
        10: (8, 15),
        15: (10, 37),
        20: (12, 63),
        25: (14, 84),
        30: (16, 95),
        33: (19, 99),
    },
    "vocabulario": {
        0: (1, 1),
        5: (5, 5),
        10: (8, 25),
        15: (10, 50),
        20: (12, 75),
        25: (14, 91),
        30: (16, 98),
        36: (19, 99),
    },
    "compreensao": {
        0: (1, 1),
        5: (6, 9),
        10: (9, 37),
        15: (11, 63),
        20: (13, 84),
        25: (15, 95),
        28: (19, 99),
    },
    "cubos": {
        0: (1, 1),
        10: (6, 9),
        20: (9, 37),
        30: (11, 63),
        40: (13, 84),
        50: (15, 95),
        60: (17, 98),
        68: (19, 99),
    },
    "conceitos_figurativos": {
        0: (1, 1),
        5: (6, 9),
        10: (9, 37),
        15: (11, 63),
        20: (13, 84),
        25: (15, 95),
        28: (19, 99),
    },
    "raciocinio_matricial": {
        0: (1, 1),
        5: (6, 9),
        10: (9, 37),
        15: (11, 63),
        20: (13, 84),
        25: (15, 95),
        30: (17, 98),
        35: (19, 99),
    },
    "digitos": {
        0: (1, 1),
        5: (5, 5),
        10: (8, 25),
        15: (10, 50),
        20: (12, 75),
        25: (14, 91),
        30: (16, 95),
        36: (18, 99),
        42: (19, 99),
    },
    "sequencias_letras_numeros": {
        0: (1, 1),
        5: (6, 9),
        10: (9, 37),
        15: (11, 63),
        20: (13, 84),
        25: (15, 95),
        30: (17, 98),
        44: (19, 99),
    },
    "codigos": {
        0: (1, 1),
        10: (5, 5),
        20: (8, 25),
        35: (10, 50),
        50: (12, 75),
        65: (14, 91),
        80: (16, 95),
        100: (18, 99),
        119: (19, 99),
    },
    "pesquisas_simbolos": {
        0: (1, 1),
        10: (6, 9),
        20: (9, 37),
        30: (11, 63),
        40: (13, 84),
        50: (15, 95),
        60: (19, 99),
    },
}

INDEX_CONVERSION: dict[int, tuple[int, str]] = {
    55: (0, "Extremamente Baixo"),
    60: (1, "Extremamente Baixo"),
    65: (1, "Extremamente Baixo"),
    70: (2, "Muito Baixo"),
    75: (5, "Muito Baixo"),
    80: (10, "Baixo"),
    85: (16, "Baixo"),
    90: (25, "Médio-Baixo"),
    95: (37, "Médio-Baixo"),
    100: (50, "Médio"),
    105: (63, "Médio"),
    110: (75, "Médio-Alto"),
    115: (84, "Médio-Alto"),
    120: (91, "Superior"),
    125: (95, "Superior"),
    130: (98, "Muito Superior"),
    135: (99, "Muito Superior"),
    140: (99, "Muito Superior"),
    145: (99, "Extremamente Superior"),
    150: (99, "Extremamente Superior"),
}

QI_CONVERSION: dict[int, tuple[int, str]] = INDEX_CONVERSION.copy()


def convert_raw_to_standard(subtest_code: str, escore_bruto: int) -> tuple[int, int]:
    table = CONVERSION_TABLE.get(subtest_code, {})
    keys = sorted(table.keys())

    for key in keys:
        if escore_bruto <= key:
            return table[key]

    if keys:
        return table[keys[-1]]
    return (10, 50)


def get_classification(escore_padrao: int) -> str:
    if escore_padrao <= 4:
        return "Muito Baixo"
    elif escore_padrao <= 6:
        return "Baixo"
    elif escore_padrao <= 8:
        return "Médio-Baixo"
    elif escore_padrao <= 12:
        return "Médio"
    elif escore_padrao <= 14:
        return "Médio-Alto"
    elif escore_padrao <= 16:
        return "Superior"
    else:
        return "Muito Superior"


def calculate_index_score(standard_scores: list[int]) -> int:
    if not standard_scores:
        return 100
    media = sum(standard_scores) / len(standard_scores)
    return int(round((media - 10) * 10 + 100))


def calculate_qi_total(index_scores: list[int]) -> int:
    if not index_scores:
        return 100
    soma = sum(index_scores)
    media = soma / len(index_scores)
    qi = int(round(media + (media - 100) * 0.25))
    return max(40, min(160, qi))


def classify_index(escore_composto: int) -> tuple[int, str]:
    keys = sorted(INDEX_CONVERSION.keys())
    for key in keys:
        if escore_composto <= key:
            return INDEX_CONVERSION[key]
    return (99, "Extremamente Superior")


def classify_qi(qi_total: int) -> tuple[int, str]:
    keys = sorted(QI_CONVERSION.keys())
    for key in keys:
        if qi_total <= key:
            return QI_CONVERSION[key]
    return (99, "Extremamente Superior")


def calculate_confidence_interval(escore: int, sem: float = 3.0) -> tuple[int, int]:
    lower = int(round(escore - 1.96 * sem))
    upper = int(round(escore + 1.96 * sem))
    return (lower, upper)
