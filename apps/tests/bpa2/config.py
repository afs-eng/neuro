from enum import Enum
from dataclasses import dataclass


class SubtestCode(str, Enum):
    CONCENTRADA = "ac"
    DIVIDIDA = "ad"
    ALTERNADA = "aa"
    GERAL = "ag"


@dataclass
class SubtestConfig:
    code: str
    name: str
    is_composite: bool = False


BPA2_SUBTESTS: dict[str, SubtestConfig] = {
    "ac": SubtestConfig(code="ac", name="Atenção Concentrada"),
    "ad": SubtestConfig(code="ad", name="Atenção Dividida"),
    "aa": SubtestConfig(code="aa", name="Atenção Alternada"),
    "ag": SubtestConfig(code="ag", name="Atenção Geral", is_composite=True),
}

BPA2_CODE = "bpa2"
BPA2_NAME = "BPA-2 - Bateria de Provas Neuropsicológicas de Atenção"
BPA2_VERSION = "2"

NORMS_DIR_RELATIVE = "apps/tests/norms/tabelas_bpa2"
