def get_severity_level(classificacao: str) -> int:
    levels = {
        "Comportamento positivo 1": 1,
        "Comportamento positivo 2": 2,
        "Com sintomatologia leve": 3,
        "Com sintomatologia moderada": 4,
        "Com sintomatologia grave ou severa": 5,
    }
    return levels.get(classificacao, 0)


def find_critical_items(detalhe_itens: list[dict]) -> list[dict]:
    critical = []
    for d in detalhe_itens:
        if d["corrigido"] == 2:
            critical.append(d)
    return critical
