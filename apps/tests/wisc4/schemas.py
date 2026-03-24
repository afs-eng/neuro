from enum import Enum
from pydantic import BaseModel, Field
from .config import IndexCode


class ClassificationLevel(str, Enum):
    MUITO_SUPERIOR = "muito_superior"
    SUPERIOR = "superior"
    MEDIA_SUPERIOR = "media_superior"
    MEDIA = "media"
    MEDIA_INFERIOR = "media_inferior"
    INFERIOR = "inferior"
    MUITO_INFERIOR = "muito_inferior"


class SubtestRawInput(BaseModel):
    escore_bruto: int = Field(ge=0)


class WISC4RawInput(BaseModel):
    semelhancas: SubtestRawInput
    vocabulario: SubtestRawInput
    compreensao: SubtestRawInput
    cubos: SubtestRawInput
    conceitos_figurativos: SubtestRawInput
    raciocinio_matricial: SubtestRawInput
    digitos: SubtestRawInput
    sequencias_letras_numeros: SubtestRawInput
    codigos: SubtestRawInput
    pesquisas_simbolos: SubtestRawInput


class SubtestResult(BaseModel):
    subteste: str
    escore_bruto: int
    escore_padrao: int
    percentil: int
    classificacao: str
    intervalo_confianca_95: tuple[int, int]


class IndexResult(BaseModel):
    indice: IndexCode
    nome: str
    escore_composto: int
    percentil: int
    classificacao: str
    subtestes: list[SubtestResult]
    intervalo_confianca_95: tuple[int, int]


class WISC4Result(BaseModel):
    subtestes: list[SubtestResult]
    indices: list[IndexResult]
    qi_total: int
    percentil_qi: int
    classificacao_qi: str
    intervalo_confianca_95: tuple[int, int]
    pontos_fortes: list[str]
    pontos_fragilizados: list[str]
    diferencas_significativas: list[str]
