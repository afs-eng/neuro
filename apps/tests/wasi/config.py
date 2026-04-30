from __future__ import annotations


WASI_CODE = "wasi"
WASI_NAME = "WASI - Escala Wechsler Abreviada de Inteligência"

WASI_MIN_AGE = 6
WASI_MAX_AGE = 89

WASI_SUBTESTS = {
    "vc": {"code": "VC", "name": "Vocabulário"},
    "sm": {"code": "SM", "name": "Semelhanças"},
    "cb": {"code": "CB", "name": "Cubos"},
    "rm": {"code": "RM", "name": "Raciocínio Matricial"},
}

WASI_COMPOSITES = {
    "qi_verbal": {
        "name": "Q.I Verbal",
        "subtests": ["vc", "sm"],
        "table": "verbal",
        "interpretability_gap": 5,
        "interpretability_message": "Pode não representar adequadamente o desempenho verbal porque ha discrepancia >= 5 pontos ponderados entre VC e SM.",
    },
    "qi_execucao": {
        "name": "Q.I. Execução",
        "subtests": ["cb", "rm"],
        "table": "execution",
        "interpretability_gap": 5,
        "interpretability_message": "Pode não representar adequadamente o desempenho de execucao porque ha discrepancia >= 5 pontos ponderados entre CB e RM.",
    },
    "qit_4": {
        "name": "Escala Total (Q.I.T. 4 subtestes)",
        "subtests": ["vc", "sm", "cb", "rm"],
        "table": "total_4",
        "interpretability_gap": 23,
        "interpretability_message": "Talvez o QIT-4 nao represente adequadamente o desempenho cognitivo porque ha discrepancia >= 23 pontos compostos entre o QI Verbal e o QI Execucao.",
    },
    "qit_2": {
        "name": "Escala Total (Q.I.T. 2 subtestes)",
        "subtests": ["vc", "rm"],
        "table": "total_2",
        "interpretability_gap": 5,
        "interpretability_message": "Talvez o QIT-2 nao represente adequadamente o desempenho cognitivo porque ha discrepancia >= 5 pontos ponderados entre VC e RM.",
    },
}


def classify_composite_score(score: int | None) -> str | None:
    if score is None:
        return None
    if score >= 130:
        return "Muito Superior"
    if score >= 120:
        return "Superior"
    if score >= 110:
        return "Média Superior"
    if score >= 90:
        return "Média"
    if score >= 80:
        return "Média Inferior"
    if score >= 70:
        return "Limítrofe"
    return "Extremamente Baixo"


def classify_subtest_z_score(z_score: float | None) -> str | None:
    if z_score is None:
        return None
    if z_score >= 2:
        return "Muito Superior"
    if z_score >= 1.333:
        return "Superior"
    if z_score >= 0.666:
        return "Média Superior"
    if z_score >= -0.666:
        return "Média"
    if z_score >= -1.333:
        return "Média Inferior"
    if z_score >= -2:
        return "Limítrofe"
    return "Deficitário"
