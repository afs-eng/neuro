import os
import csv
from .config import NORMS_DIR_RELATIVE


FAIXAS_ETARIAS = [
    "6 anos",
    "7 anos",
    "8 anos",
    "9 anos",
    "10 anos",
    "11 anos",
    "12 anos",
    "13 anos",
    "14 anos",
    "15-17 anos",
    "18-20 anos",
    "21-30 anos",
    "31-40 anos",
    "41-50 anos",
    "51-60 anos",
    "61-70 anos",
    "71-80 anos",
    "81 anos ou mais",
]


def get_norms_dir() -> str:
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    return os.path.join(base, NORMS_DIR_RELATIVE)


def load_table(code: str, mode: str) -> list[dict]:
    suffix = "age" if mode == "idade" else "escolaridade"
    filename = f"{code}_{suffix}.csv"
    filepath = os.path.join(get_norms_dir(), filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Tabela não encontrada: {filepath}")

    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader)


def get_age_group(age: int) -> str:
    if age < 6:
        raise ValueError("Idade mínima para o BPA-2 é 6 anos")
    if age <= 14:
        return f"{age} anos"
    if age <= 17:
        return "15-17 anos"
    if age <= 20:
        return "18-20 anos"
    if age <= 30:
        return "21-30 anos"
    if age <= 40:
        return "31-40 anos"
    if age <= 50:
        return "41-50 anos"
    if age <= 60:
        return "51-60 anos"
    if age <= 70:
        return "61-70 anos"
    if age <= 80:
        return "71-80 anos"
    return "81 anos ou mais"


def classify_score(
    escore_total: int, tabela: list[dict], faixa: str
) -> tuple[str, int]:
    for row in tabela:
        valor = row.get(faixa)
        if valor is None:
            continue
        try:
            valor_int = int(valor)
        except ValueError:
            continue
        if escore_total <= valor_int:
            return row["classificação"], int(row["Percentil"])

    ultimo = tabela[-1]
    return ultimo["classificação"], int(ultimo["Percentil"])


def calculate_total(brutos: int, erros: int, omissoes: int) -> int:
    return brutos - erros - omissoes
