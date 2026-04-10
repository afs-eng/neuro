from .config import ITENS_POSITIVOS, ITENS_NEGATIVOS

TABELA_AMOSTRA_GERAL = {
    0: ("<1", 19, 1),
    1: ("<1", 20, 1),
    2: (4, 21, 1),
    3: (4, 22, 1),
    4: (4, 23, 1),
    5: (4, 24, 1),
    6: (4, 25, 1),
    7: (4, 26, 1),
    8: (4, 27, 1),
    9: (4, 28, 1),
    10: (4, 29, 1),
    11: (5, 30, 1),
    12: (5, 31, 1),
    13: (5, 32, 1),
    14: (5, 33, 1),
    15: (6, 34, 1),
    16: (6, 35, 2),
    17: (7, 36, 2),
    18: (7, 37, 2),
    19: (8, 38, 2),
    20: (10, 39, 2),
    21: (11, 40, 3),
    22: (13, 41, 3),
    23: (15, 42, 3),
    24: (18, 43, 3),
    25: (21, 44, 3),
    26: (25, 45, 4),
    27: (29, 46, 4),
    28: (35, 47, 4),
    29: (41, 48, 4),
    30: (48, 49, 4),
    31: (55, 50, 5),
    32: (63, 51, 5),
    33: (69, 52, 5),
    34: (74, 53, 5),
    35: (78, 54, 5),
    36: (81, 55, 6),
    37: (83, 56, 6),
    38: (85, 57, 6),
    39: (86, 58, 6),
    40: (87, 60, 6),
    41: (88, 61, 7),
    42: (89, 62, 7),
    43: (90, 63, 7),
    44: (91, 64, 7),
    45: (92, 65, 7),
    46: (93, 66, 8),
    47: (94, 67, 8),
    48: (95, 68, 8),
    49: (96, 69, 8),
    50: (97, 70, 8),
    51: (98, 71, 9),
    52: (99, 72, 9),
    53: (99, 73, 9),
    54: (">99", 74, 9),
}


def corrigir_item(item: int, resposta: int) -> int:
    if item in ITENS_POSITIVOS:
        return 2 - resposta
    return resposta


def calcular_pontuacoes(respostas: list[int]) -> dict:
    soma_negativos = 0
    soma_positivos = 0
    detalhes = []

    for item in range(1, 28):
        original = respostas[item - 1]
        corrigido = corrigir_item(item, original)

        if item in ITENS_POSITIVOS:
            soma_positivos += corrigido
        else:
            soma_negativos += corrigido

        detalhes.append(
            {
                "item": item,
                "resposta": original,
                "invertido": item in ITENS_POSITIVOS,
                "corrigido": corrigido,
            }
        )

    pontuacao_total = soma_negativos + soma_positivos

    return {
        "soma_itens_negativos": soma_negativos,
        "soma_itens_positivos": soma_positivos,
        "pontuacao_total": pontuacao_total,
        "detalhe_itens": detalhes,
    }


def classificar_tabela_18(pontuacao_total: int) -> str:
    if 0 <= pontuacao_total <= 15:
        return "Sintomatologia mínima"
    if 16 <= pontuacao_total <= 20:
        return "Sintomatologia mínima (presença de indicadores isolados)"
    if 21 <= pontuacao_total <= 30:
        return "Sintomatologia Leve (ou sem sintomas clinicamente relevantes)"
    if 31 <= pontuacao_total <= 45:
        return "Sintomatologia Moderada"
    if 46 <= pontuacao_total <= 54:
        return "Sintomatologia Grave ou Severa"
    return "Pontuação fora do intervalo esperado (0-54)"


def obter_normas(pontuacao_total: int) -> dict | None:
    normas = TABELA_AMOSTRA_GERAL.get(pontuacao_total)
    if normas is None:
        return None
    return {
        "percentil": normas[0],
        "T": normas[1],
        "estanino": normas[2],
    }
