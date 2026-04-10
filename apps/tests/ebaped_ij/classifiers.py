def get_severity_level(classificacao: str) -> int:
    levels = {
        "Sintomatologia mínima": 1,
        "Sintomatologia mínima (presença de indicadores isolados)": 2,
        "Sintomatologia Leve (ou sem sintomas clinicamente relevantes)": 3,
        "Sintomatologia Moderada": 4,
        "Sintomatologia Grave ou Severa": 5,
    }
    return levels.get(classificacao, 0)


def find_critical_items(detalhe_itens: list[dict]) -> list[dict]:
    critical = []
    for d in detalhe_itens:
        if d["corrigido"] == 2:
            critical.append(d)
    return critical
