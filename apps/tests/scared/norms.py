import math

PAIS_CORTES = {
    "panico_sintomas_somaticos": 7,
    "ansiedade_generalizada": 9,
    "ansiedade_separacao": 5,
    "fobia_social": 8,
    "evitacao_escolar": 3,
    "total": 25,
}

AUTORRELATO_NORMAS = {
    "crianca": {
        "masculino": {
            "total": {"media": 22.6, "dp": 10.45},
            "panico_sintomas_somaticos": {"media": 4.16, "dp": 3.8},
            "ansiedade_generalizada": {"media": 7.24, "dp": 3.57},
            "ansiedade_separacao": {"media": 4.98, "dp": 2.65},
            "fobia_social": {"media": 4.98, "dp": 2.83},
            "evitacao_escolar": {"media": 1.24, "dp": 1.19},
        },
        "feminino": {
            "total": {"media": 26.55, "dp": 12.21},
            "panico_sintomas_somaticos": {"media": 5.36, "dp": 4.69},
            "ansiedade_generalizada": {"media": 8.03, "dp": 3.7},
            "ansiedade_separacao": {"media": 6.03, "dp": 3.22},
            "fobia_social": {"media": 5.74, "dp": 2.92},
            "evitacao_escolar": {"media": 1.39, "dp": 1.3},
        },
    },
    "adolescente": {
        "masculino": {
            "total": {"media": 19.73, "dp": 10.41},
            "panico_sintomas_somaticos": {"media": 3.29, "dp": 3.4},
            "ansiedade_generalizada": {"media": 7.51, "dp": 3.73},
            "ansiedade_separacao": {"media": 3.55, "dp": 2.36},
            "fobia_social": {"media": 4.43, "dp": 2.95},
            "evitacao_escolar": {"media": 0.94, "dp": 1.14},
        },
        "feminino": {
            "total": {"media": 25.69, "dp": 12.17},
            "panico_sintomas_somaticos": {"media": 5.34, "dp": 4.58},
            "ansiedade_generalizada": {"media": 8.87, "dp": 3.78},
            "ansiedade_separacao": {"media": 4.78, "dp": 2.86},
            "fobia_social": {"media": 5.46, "dp": 3.2},
            "evitacao_escolar": {"media": 1.24, "dp": 1.21},
        },
    },
}


def normal_cdf(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def percentil_para_classificacao(percentil: float) -> str:
    if percentil >= 95:
        return "Muito Elevado"
    if percentil >= 75:
        return "Elevado"
    if percentil >= 25:
        return "Na Média"
    if percentil >= 10:
        return "Médio Inferior"
    if percentil >= 5:
        return "Baixo"
    return "Muito Baixo"
