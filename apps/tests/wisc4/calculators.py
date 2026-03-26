import re
import csv
from pathlib import Path

from .paths import TABELAS_NCP, TABELAS_EQUIVALENTES


WISC4_CODE = "wisc4"
WISC4_NAME = "WISC-IV - Escala de Inteligência Wechsler para Crianças"
WISC4_VERSION = "4"

WISC4_SUBTESTS = {
    "semelhancas": {"name": "Semelhanças", "code": "SM", "max": 33},
    "vocabulario": {"name": "Vocabulário", "code": "VC", "max": 36},
    "compreensao": {"name": "Compreensão", "code": "CO", "max": 28},
    "cubos": {"name": "Cubos", "code": "CB", "max": 68},
    "conceitos": {"name": "Conceitos Figurativos", "code": "CN", "max": 28},
    "matricial": {"name": "Raciocínio Matricial", "code": "RM", "max": 35},
    "digitos": {"name": "Dígitos", "code": "DG", "max": 42},
    "sequencias": {"name": "Seq. Letras e Números", "code": "SNL", "max": 44},
    "codigos": {"name": "Códigos", "code": "CD", "max": 119},
    "procura_simbolos": {"name": "Procura de Símbolos", "code": "PS", "max": 60},
}

WISC4_INDICES = {
    "icv": {
        "name": "Índice de Compreensão Verbal",
        "subtests": ["semelhancas", "vocabulario", "compreensao"],
    },
    "iop": {
        "name": "Índice de Organização Perceptual",
        "subtests": ["cubos", "conceitos", "matricial"],
    },
    "imt": {
        "name": "Índice de Memória de Trabalho",
        "subtests": ["digitos", "sequencias"],
    },
    "ivp": {
        "name": "Índice de Velocidade de Processamento",
        "subtests": ["codigos", "procura_simbolos"],
    },
}

INDEX_CONVERSION = {
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


def _idade_em_meses(anos: int, meses: int) -> int:
    return anos * 12 + meses


def _calcular_idade(birth_date, evaluation_date) -> tuple[int, int]:
    anos = evaluation_date.year - birth_date.year
    meses = evaluation_date.month - birth_date.month
    if evaluation_date.day < birth_date.day:
        meses -= 1
    if meses < 0:
        anos -= 1
        meses += 12
    return anos, meses


def _obter_arquivo_ncp(anos: int, meses: int) -> Path:
    idade_meses = _idade_em_meses(anos, meses)
    faixas = []
    for arquivo in TABELAS_NCP.glob("idade_*.csv"):
        match = re.match(r"idade_(\d+)-(\d+)-(\d+)-(\d+)$", arquivo.stem)
        if not match:
            match = re.match(r"idade_(\d+)-(\d+)_(\d+)-(\d+)$", arquivo.stem)
        if not match:
            continue
        a1, m1, a2, m2 = map(int, match.groups())
        min_meses = _idade_em_meses(a1, m1)
        max_exclusivo = _idade_em_meses(a2, m2) + 1
        faixas.append({"min": min_meses, "max": max_exclusivo, "arquivo": arquivo})

    faixas.sort(key=lambda f: f["min"])
    for faixa in faixas:
        if faixa["min"] <= idade_meses < faixa["max"]:
            return faixa["arquivo"]

    raise ValueError(f"Idade fora das faixas WISC-IV: {anos}a {meses}m")


def _carregar_tabela_ncp(anos: int, meses: int) -> list[dict]:
    arquivo = _obter_arquivo_ncp(anos, meses)
    with open(arquivo, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _valor_no_intervalo(valor: int, celula: str) -> bool:
    if not celula or celula.strip() in ("", "-"):
        return False
    celula = celula.strip().replace(":", "-")
    if "-" in celula:
        try:
            inicio, fim = celula.split("-", 1)
            return int(inicio) <= valor <= int(fim)
        except (ValueError,):
            return False
    try:
        return valor == int(celula)
    except (ValueError,):
        return False


def buscar_ponderado(tabela: list[dict], coluna: str, valor_bruto: int) -> int:
    for linha in tabela:
        celula = linha.get(coluna, "")
        if _valor_no_intervalo(valor_bruto, celula):
            pp = linha.get("PP", "")
            if pp and pp.strip().isdigit():
                return int(pp.strip())
    raise ValueError(f"Valor bruto {valor_bruto} não encontrado para {coluna}")


def get_classification_padrao(escore_padrao: int) -> str:
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


def get_classification_composto(escore: int) -> tuple[int, str]:
    keys = sorted(INDEX_CONVERSION.keys())
    for key in keys:
        if escore <= key:
            return INDEX_CONVERSION[key]
    return (99, "Extremamente Superior")


def calculate_index_score(standard_scores: list[int]) -> int:
    if not standard_scores:
        return 0
    return sum(standard_scores)


def calculate_qi_total(index_scores: list[int]) -> int:
    if not index_scores:
        return 100
    soma = sum(index_scores)
    media = soma / len(index_scores)
    qi = int(round(media + (media - 100) * 0.25))
    return max(40, min(160, qi))


def calculate_confidence_interval(escore: int, sem: float = 3.0) -> tuple[int, int]:
    lower = int(round(escore - 1.96 * sem))
    upper = int(round(escore + 1.96 * sem))
    return (lower, upper)


EQUIVALENCE_TABLE_FILES = {
    "icv": "tabela A2.csv",
    "iop": "tabela A3.csv",
    "imt": "tabela A4.csv",
    "ivp": "tabela A5.csv",
    "qit": "Tabela A6.csv",
}

EQUIVALENCE_TABLE_COLUMNS = {
    "icv": "ICV",
    "iop": "IOP",
    "imt": "IMO",
    "ivp": "IVP",
    "qit": "QIT",
}


def _carregar_tabela_equivalente(index_code: str) -> list[dict]:
    arquivo = TABELAS_EQUIVALENTES / EQUIVALENCE_TABLE_FILES[index_code]
    with open(arquivo, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _parse_percentile(percentil_str: str) -> float:
    percentil_str = percentil_str.strip().replace(",", ".")
    if percentil_str.startswith("<"):
        return 0.01
    if percentil_str.startswith(">"):
        return 99.9
    try:
        return float(percentil_str)
    except (ValueError,):
        return 0.0


def _parse_interval(interval_str: str) -> tuple[int, int]:
    interval_str = interval_str.strip()
    if not interval_str or interval_str == "-":
        return (0, 0)
    parts = interval_str.split("-")
    if len(parts) == 2:
        return (int(parts[0]), int(parts[1]))
    return (0, 0)


def lookup_composite_score(index_code: str, soma_ponderados: int) -> dict:
    """
    Lookup composite score, percentile, and confidence intervals from equivalence table.
    index_code: 'icv', 'iop', 'imt', 'ivp', 'qit'
    Returns: {'escore': int, 'percentil': float, 'ic_90': tuple, 'ic_95': tuple}
    """
    tabela = _carregar_tabela_equivalente(index_code)
    score_column = EQUIVALENCE_TABLE_COLUMNS.get(index_code, index_code.upper())
    for linha in tabela:
        soma_col = linha.get("Soma dos pontos ponderados", "").strip()
        if not soma_col:
            continue
        try:
            if int(soma_col) == soma_ponderados:
                escore = int(linha.get(score_column, "0").strip())
                percentil = _parse_percentile(linha.get("Rank Percentil", "0"))
                ic_90 = _parse_interval(linha.get("90%", "0-0"))
                ic_95 = _parse_interval(linha.get("95%", "0-0"))
                return {
                    "escore": escore,
                    "percentil": percentil,
                    "ic_90": ic_90,
                    "ic_95": ic_95,
                }
        except ValueError, KeyError:
            continue
    raise ValueError(f"Soma {soma_ponderados} não encontrada para {index_code}")


def lookup_gai_score(soma_ponderados: int) -> dict:
    """
    Lookup GAI (General Ability Index) from Tabela-GAI.csv.
    Returns: {'escore': int, 'percentil': float, 'ic_95': tuple, 'classificacao': str}
    """
    arquivo = TABELAS_EQUIVALENTES / "Tabela-GAI.csv"
    with open(arquivo, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for linha in reader:
            soma_col = linha.get("Soma de Escalado Pontuações", "").strip()
            if not soma_col:
                continue
            try:
                if int(soma_col) == soma_ponderados:
                    escore = int(linha.get("GAI", "0").strip())
                    percentil = _parse_percentile(linha.get("Percentil", "0"))
                    ic_95 = _parse_interval(linha.get("Nível de Confiança 95%", "0-0"))
                    _, classificacao = get_classification_composto(escore)
                    return {
                        "escore": escore,
                        "percentil": percentil,
                        "ic_95": ic_95,
                        "classificacao": classificacao,
                    }
            except ValueError, KeyError:
                continue
    raise ValueError(f"Soma {soma_ponderados} não encontrada para GAI")


def lookup_cpi_score(soma_ponderados: int) -> dict:
    """
    Lookup CPI (Cognitive Proficiency Index) from Tabela-CPI.csv.
    Returns: {'escore': int, 'percentil': float, 'ic_95': tuple, 'classificacao': str}
    """
    arquivo = TABELAS_EQUIVALENTES / "Tabela-CPI.csv"
    with open(arquivo, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for linha in reader:
            soma_col = linha.get("Soma de Escalas", "").strip()
            if not soma_col:
                continue
            try:
                if int(soma_col) == soma_ponderados:
                    escore = int(linha.get("CPI", "0").strip())
                    percentil = _parse_percentile(linha.get("Percentil", "0"))
                    ic_95 = _parse_interval(linha.get("IC 95%", "0-0"))
                    _, classificacao = get_classification_composto(escore)
                    return {
                        "escore": escore,
                        "percentil": percentil,
                        "ic_95": ic_95,
                        "classificacao": classificacao,
                    }
            except ValueError, KeyError:
                continue
    raise ValueError(f"Soma {soma_ponderados} não encontrada para CPI")
