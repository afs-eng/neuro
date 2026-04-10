
from enum import Enum


class ReportSectionKey(str, Enum):
    IDENTIFICACAO = "identificacao"
    DEMANDA = "demanda"
    PROCEDIMENTOS = "procedimentos"
    HISTORIA_PESSOAL = "historia_pessoal"
    CAPACIDADE_COGNITIVA_GLOBAL = "capacidade_cognitiva_global"
    FUNCOES_EXECUTIVAS = "funcoes_executivas"
    LINGUAGEM = "linguagem"
    GNOSIAS_PRAXIAS = "gnosias_praxias"
    MEMORIA_APRENDIZAGEM = "memoria_aprendizagem"
    ATENCAO = "atencao"
    RAVLT = "ravlt"
    FDT = "fdt"
    ETDAH_PAIS = "etdah_pais"
    ETDAH_AD = "etdah_ad"
    SCARED = "scared"
    EPQJ = "epqj"
    SRS2 = "srs2"
    CONCLUSAO = "conclusao"
    CONDUTA = "conduta"
    FECHAMENTO = "fechamento"
    REFERENCIAS = "referencias"


class GenerationMode(str, Enum):
    TEMPLATE = "template"
    LLM = "llm"
    HYBRID = "hybrid"
