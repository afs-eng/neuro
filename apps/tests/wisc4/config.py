from enum import Enum
from dataclasses import dataclass


class IndexCode(str, Enum):
    ICV = "icv"
    IOP = "iop"
    IMT = "imt"
    IVP = "ivp"


@dataclass
class SubtestConfig:
    code: str
    name: str
    index: IndexCode
    max_raw_score: int


@dataclass
class IndexConfig:
    code: IndexCode
    name: str
    subtests: list[str]


WISC4_SUBTESTS: dict[str, SubtestConfig] = {
    "semelhancas": SubtestConfig("semelhancas", "Semelhanças", IndexCode.ICV, 33),
    "vocabulario": SubtestConfig("vocabulario", "Vocabulário", IndexCode.ICV, 36),
    "compreensao": SubtestConfig("compreensao", "Compreensão", IndexCode.ICV, 28),
    "cubos": SubtestConfig("cubos", "Cubos", IndexCode.IOP, 68),
    "conceitos_figurativos": SubtestConfig(
        "conceitos_figurativos", "Conceitos Figurativos", IndexCode.IOP, 28
    ),
    "raciocinio_matricial": SubtestConfig(
        "raciocinio_matricial", "Raciocínio Matricial", IndexCode.IOP, 35
    ),
    "digitos": SubtestConfig("digitos", "Dígitos", IndexCode.IMT, 42),
    "sequencias_letras_numeros": SubtestConfig(
        "sequencias_letras_numeros", "Sequências de Letras e Números", IndexCode.IMT, 44
    ),
    "codigos": SubtestConfig("codigos", "Códigos", IndexCode.IVP, 119),
    "pesquisas_simbolos": SubtestConfig(
        "pesquisas_simbolos", "Pesquisas de Símbolos", IndexCode.IVP, 60
    ),
}

WISC4_INDICES: dict[IndexCode, IndexConfig] = {
    IndexCode.ICV: IndexConfig(
        IndexCode.ICV,
        "Índice de Compreensão Verbal",
        ["semelhancas", "vocabulario", "compreensao"],
    ),
    IndexCode.IOP: IndexConfig(
        IndexCode.IOP,
        "Índice de Organização Perceptual",
        ["cubos", "conceitos_figurativos", "raciocinio_matricial"],
    ),
    IndexCode.IMT: IndexConfig(
        IndexCode.IMT,
        "Índice de Memória de Trabalho",
        ["digitos", "sequencias_letras_numeros"],
    ),
    IndexCode.IVP: IndexConfig(
        IndexCode.IVP,
        "Índice de Velocidade de Processamento",
        ["codigos", "pesquisas_simbolos"],
    ),
}

WISC4_CODE = "wisc4"
WISC4_NAME = "Escala de Inteligência Wechsler para Crianças - IV Edição"
WISC4_VERSION = "4"
