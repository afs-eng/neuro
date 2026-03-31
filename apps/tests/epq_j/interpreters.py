INTERPRETACOES = {
    "P": {
        "MUITO BAIXO": "Tendência muito baixa à personalidade psicótica. Indicaausência de traços significativos de desorganizaçãoou comportamento anti-social.",
        "BAIXO": "Baixa tendência à personalidade psicótica. Comportamento relativamente organizado e socializado.",
        "MEDIO": "Nível médio de traços de personalidade. Comportamento dentro dos padrões esperados.",
        "ALTO": "Elevada tendência à personalidade psicótica. May indicate difficulties with impulse control and social behavior.",
        "MUITO ALTO": "Muito elevada tendência à personalidade psicótica. Requer avaliação clínica aprofundada.",
    },
    "E": {
        "MUITO BAIXO": "Extroversão muito baixa. Indivíduo introvertido, reserved, prefere atividades individuais.",
        "BAIXO": "Baixa extroversão. Tendência à introversão com menor busca de estímulos sociais.",
        "MEDIO": "Nível médio de extroversão. Balanço entre introversão e extroversão.",
        "ALTO": "Elevada extroversão. Indivíduo sociável, comunicativo e busca de estímulos.",
        "MUITO ALTO": "Muito elevada extroversão. Extrovertido marcado, muito sociável e ativo.",
    },
    "N": {
        "MUITO BAIXO": "Neuroticismo muito baixo. Muito estável emocionalmente, calma e equilibraduado.",
        "BAIXO": "Baixo neuroticismo. Estável emocionalmente, não reage intensamente ao estresse.",
        "MEDIO": "Nível médio de neuroticismo. Reações emocionais dentro dos padrões normais.",
        "ALTO": "Elevado neuroticismo. Tendência à instabilidade emocional e reações intensas.",
        "MUITO ALTO": "Muito elevado neuroticismo. Instabilidade emocional significativa, ansiedadeelevada.",
    },
    "S": {
        "MUITO BAIXO": "Socialização muito baixa. Dificuldades significativas no relacionamento social.",
        "BAIXO": "Baixa socialização. Dificuldades de integração social.",
        "MEDIO": "Nível médio de socialização. Relacionamentos sociais dentro dos padrões.",
        "ALTO": "Elevada socialização. Boa capacidade de integração e relacionamento social.",
        "MUITO ALTO": "Muito elevada socialização. Excelente capacidade de relacionamento social.",
    },
}


def interpret_result(fator: str, classificacao: str) -> str:
    return INTERPRETACOES.get(fator, {}).get(classificacao, "")


def get_synthesis(resultado: dict) -> str:
    parts = []
    for fator in ["P", "E", "N", "S"]:
        if fator in resultado:
            r = resultado[fator]
            parts.append(f"{fator}: {r['classificacao']} (P{r['percentil']})")
    return " | ".join(parts)


def get_report_interpretation(result: dict) -> str:
    lines = []
    for fator in ["P", "E", "N", "S"]:
        if fator in result:
            r = result[fator]
            interp = interpret_result(fator, r["classificacao"])
            lines.append(
                f"\n{fator} - {r['classificacao']} (Escore: {r['escore']}, Percentil: {r['percentil']})"
            )
            lines.append(f"   {interp}")
    return "\n".join(lines)
