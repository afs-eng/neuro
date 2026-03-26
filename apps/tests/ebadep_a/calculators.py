from .config import TABELA_PERCENTIS


def calcular_escore(respostas: list[int]) -> int:
    return sum(respostas)


def obter_percentil(escore: int) -> int:
    return TABELA_PERCENTIS.get(escore, 99)


def classificar(escore: int) -> str:
    if 0 <= escore <= 59:
        return "Sintomatologia Depressiva Mínima (sem sintomatologia)"
    if 60 <= escore <= 76:
        return "Sintomatologia Depressiva Leve"
    if 77 <= escore <= 110:
        return "Sintomatologia Depressiva Moderada"
    if 111 <= escore <= 135:
        return "Sintomatologia Depressiva Severa"
    return "Escore fora da faixa válida"
