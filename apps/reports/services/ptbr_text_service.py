import re


class PtBrTextService:
    PHRASE_REPLACEMENTS = [
        (r"\bA IA nao esta disponivel no momento\b", "A IA não está disponível no momento"),
        (r"\bNao ha\b", "Não há"),
        (r"\bnao ha\b", "não há"),
        (r"\bNao foi possivel\b", "Não foi possível"),
        (r"\bnao foi possivel\b", "não foi possível"),
        (r"\bEm analise clinica\b", "Em análise clínica"),
    ]

    WORD_REPLACEMENTS = {
        "nao": "não",
        "tambem": "também",
        "alem": "além",
        "porem": "porém",
        "clinica": "clínica",
        "clinico": "clínico",
        "clinicos": "clínicos",
        "tecnica": "técnica",
        "tecnicas": "técnicas",
        "tecnico": "técnico",
        "tecnicos": "técnicos",
        "secao": "seção",
        "secoes": "seções",
        "avaliacao": "avaliação",
        "avaliacoes": "avaliações",
        "descricao": "descrição",
        "conclusao": "conclusão",
        "hipotese": "hipótese",
        "historia": "história",
        "memoria": "memória",
        "atencao": "atenção",
        "interacao": "interação",
        "interacoes": "interações",
        "comunicacao": "comunicação",
        "informacao": "informação",
        "informacoes": "informações",
        "possivel": "possível",
        "possiveis": "possíveis",
        "analise": "análise",
        "diagnostico": "diagnóstico",
        "diagnosticos": "diagnósticos",
        "neuropsicologico": "neuropsicológico",
        "neuropsicologica": "neuropsicológica",
        "psicologico": "psicológico",
        "psicologica": "psicológica",
        "psiquiatrico": "psiquiátrico",
        "psiquiatricos": "psiquiátricos",
        "auxilio": "auxílio",
        "conteudo": "conteúdo",
        "cognicao": "cognição",
        "percepcao": "percepção",
        "restritos": "restritos",
        "repetitivos": "repetitivos",
        "funcoes": "funções",
        "linguistico": "linguístico",
        "linguistica": "linguística",
        "inibitorio": "inibitório",
        "dominio": "domínio",
        "dominios": "domínios",
        "transtorno": "transtorno",
        "espectro": "espectro",
        "criterio": "critério",
        "criterios": "critérios",
        "metrica": "métrica",
        "metricas": "métricas",
    }

    @classmethod
    def normalize(cls, text: str | None) -> str:
        normalized = str(text or "")
        if not normalized:
            return ""

        for pattern, replacement in cls.PHRASE_REPLACEMENTS:
            normalized = re.sub(pattern, replacement, normalized)

        for raw, replacement in cls.WORD_REPLACEMENTS.items():
            normalized = re.sub(rf"\b{raw}\b", replacement, normalized)
            normalized = re.sub(rf"\b{raw.capitalize()}\b", replacement.capitalize(), normalized)
            normalized = re.sub(rf"\b{raw.upper()}\b", replacement.upper(), normalized)

        normalized = re.sub(r"[ \t]+\n", "\n", normalized)
        normalized = re.sub(r"\n{3,}", "\n\n", normalized)
        return normalized.strip()
