ITENS_EPQJ = {
    "P": [3, 7, 10, 13, 16, 21, 22, 25, 29, 32, 36, 39, 42, 54],
    "E": [8, 11, 23, 27, 31, 34, 44, 45, 50, 52, 56, 60],
    "N": [2, 5, 9, 12, 15, 18, 20, 24, 28, 35, 38, 41, 47, 49, 51, 53, 58, 59],
    "S": [1, 4, 6, 14, 17, 19, 26, 30, 33, 37, 40, 43, 46, 48, 55, 57],
}


def classificar(valor, tabela):
    for min_v, max_v, percentil, classe in tabela:
        if min_v <= valor <= max_v:
            return percentil, classe
    return "--", "NAO CLASSIFICADO"


MASCULINO = {
    "P": [
        (0, 0, 5, "MUITO BAIXO"),
        (1, 1, 20, "BAIXO"),
        (2, 2, 30, "MEDIO"),
        (3, 3, 40, "MEDIO"),
        (4, 4, 60, "MEDIO"),
        (5, 6, 70, "MEDIO"),
        (7, 7, 80, "ALTO"),
        (8, 11, 90, "ALTO"),
        (12, 14, 99, "MUITO ALTO"),
    ],
    "E": [
        (0, 4, 5, "MUITO BAIXO"),
        (5, 6, 10, "BAIXO"),
        (7, 8, 20, "BAIXO"),
        (9, 9, 30, "MEDIO"),
        (10, 10, 50, "MEDIO"),
        (11, 11, 70, "MEDIO"),
        (12, 12, 90, "ALTO"),
    ],
    "N": [
        (0, 2, 5, "MUITO BAIXO"),
        (3, 3, 10, "BAIXO"),
        (4, 5, 20, "BAIXO"),
        (6, 6, 30, "MEDIO"),
        (7, 7, 40, "MEDIO"),
        (8, 8, 50, "MEDIO"),
        (9, 9, 60, "MEDIO"),
        (10, 11, 70, "MEDIO"),
        (12, 12, 80, "ALTO"),
        (13, 16, 90, "ALTO"),
        (17, 18, 99, "MUITO ALTO"),
    ],
    "S": [
        (0, 3, 5, "MUITO BAIXO"),
        (4, 5, 10, "BAIXO"),
        (6, 6, 20, "BAIXO"),
        (7, 8, 30, "MEDIO"),
        (9, 9, 40, "MEDIO"),
        (10, 11, 50, "MEDIO"),
        (12, 12, 60, "MEDIO"),
        (13, 13, 70, "MEDIO"),
        (14, 14, 80, "ALTO"),
        (15, 15, 90, "ALTO"),
        (16, 16, 99, "MUITO ALTO"),
    ],
}


FEMININO = {
    "P": [
        (0, 0, 5, "MUITO BAIXO"),
        (1, 1, 20, "BAIXO"),
        (2, 2, 40, "MEDIO"),
        (3, 3, 60, "MEDIO"),
        (4, 4, 70, "MEDIO"),
        (5, 6, 80, "ALTO"),
        (7, 7, 90, "ALTO"),
        (8, 14, 99, "MUITO ALTO"),
    ],
    "E": [
        (0, 5, 5, "MUITO BAIXO"),
        (6, 7, 10, "BAIXO"),
        (8, 8, 20, "BAIXO"),
        (9, 9, 40, "MEDIO"),
        (10, 10, 50, "MEDIO"),
        (11, 11, 70, "MEDIO"),
        (12, 12, 90, "ALTO"),
    ],
    "N": [
        (0, 2, 5, "MUITO BAIXO"),
        (3, 4, 10, "BAIXO"),
        (5, 6, 20, "BAIXO"),
        (7, 7, 30, "MEDIO"),
        (8, 8, 40, "MEDIO"),
        (9, 9, 50, "MEDIO"),
        (10, 10, 60, "MEDIO"),
        (11, 12, 70, "MEDIO"),
        (13, 13, 80, "ALTO"),
        (14, 15, 90, "ALTO"),
        (16, 18, 99, "MUITO ALTO"),
    ],
    "S": [
        (0, 4, 5, "MUITO BAIXO"),
        (5, 5, 10, "BAIXO"),
        (6, 7, 20, "BAIXO"),
        (8, 8, 30, "MEDIO"),
        (9, 9, 40, "MEDIO"),
        (10, 10, 50, "MEDIO"),
        (11, 12, 60, "MEDIO"),
        (13, 13, 70, "MEDIO"),
        (14, 14, 80, "ALTO"),
        (15, 15, 90, "ALTO"),
        (16, 16, 99, "MUITO ALTO"),
    ],
}


def calcular_escore(respostas: dict) -> dict:
    return {
        f: sum(respostas.get(i, 0) for i in itens) for f, itens in ITENS_EPQJ.items()
    }


def obter_percentil_e_classificacao(
    escore_p: int, escore_e: int, escore_n: int, escore_s: int, sexo: str
) -> dict:
    normas = MASCULINO if sexo == "M" else FEMININO

    p_p, c_p = classificar(escore_p, normas["P"])
    p_e, c_e = classificar(escore_e, normas["E"])
    p_n, c_n = classificar(escore_n, normas["N"])
    p_s, c_s = classificar(escore_s, normas["S"])

    return {
        "P": {"escore": escore_p, "percentil": p_p, "classificacao": c_p},
        "E": {"escore": escore_e, "percentil": p_e, "classificacao": c_e},
        "N": {"escore": escore_n, "percentil": p_n, "classificacao": c_n},
        "S": {"escore": escore_s, "percentil": p_s, "classificacao": c_s},
    }
