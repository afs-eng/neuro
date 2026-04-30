from __future__ import annotations


def _first_name(patient_name: str | None) -> str:
    if not patient_name:
        return "Paciente"
    return patient_name.strip().split()[0] or "Paciente"


def build_wais3_interpretation(merged_data: dict, patient_name: str) -> str:
    first_name = _first_name(patient_name)
    indices = merged_data.get("indices") or {}
    gai = merged_data.get("gai_data") or {}
    cpi = merged_data.get("cpi_data") or {}
    discrepancias = merged_data.get("discrepancias") or []
    facilidades = merged_data.get("facilidades_dificuldades") or []
    qit = indices.get("qi_total") or {}
    qiv = indices.get("qi_verbal") or {}
    qie = indices.get("qi_execucao") or {}
    icv = indices.get("compreensao_verbal") or {}
    iop = indices.get("organizacao_perceptual") or {}
    imo = indices.get("memoria_operacional") or {}
    ivp = indices.get("velocidade_processamento") or {}

    if qit.get("pontuacao_composta") is None:
        return (
            f"Interpretação e Observações Clínicas: A avaliação da eficiência intelectual de {first_name} por meio da Escala de Inteligência Wechsler para Adultos – Terceira Edição (WAIS-III) foi registrada no sistema, porém as tabelas normativas ainda não estão preenchidas de forma suficiente para cálculo automatizado dos escores compostos, percentis e intervalos de confiança. Em análise clínica, o módulo está estruturado para receber os dados do teste, mas a interpretação quantitativa completa depende do preenchimento autorizado das tabelas normativas."
        )

    text = (
        f"Interpretação e Observações Clínicas: A avaliação da eficiência intelectual de {first_name} foi realizada por meio da Escala de Inteligência Wechsler para Adultos – Terceira Edição (WAIS-III), instrumento destinado à investigação do funcionamento intelectual global e de domínios cognitivos específicos. O desempenho indicou funcionamento intelectual global classificado como {str(qit.get('classificacao') or '').lower()}, com QI Total de {qit.get('pontuacao_composta')}, percentil {qit.get('percentil')} e intervalo de confiança de {qit.get('ic_95') or qit.get('ic_90') or '-'}. O QI Verbal apresentou classificação {str(qiv.get('classificacao') or '').lower()}, enquanto o QI de Execução situou-se em {str(qie.get('classificacao') or '').lower()}. A análise dos índices fatoriais revelou desempenho em Compreensão Verbal classificado como {str(icv.get('classificacao') or '').lower()}, Organização Perceptual como {str(iop.get('classificacao') or '').lower()}, Memória Operacional como {str(imo.get('classificacao') or '').lower()} e Velocidade de Processamento como {str(ivp.get('classificacao') or '').lower()}. Em análise clínica, o perfil cognitivo observado deve ser compreendido a partir da relação entre os índices, da presença ou ausência de discrepâncias clinicamente relevantes e da integração com os demais instrumentos da avaliação neuropsicológica."
    )

    extras: list[str] = []
    if gai.get("calculado"):
        extras.append(
            f"O índice GAI foi estimado em {gai.get('escore_composto')} ({str(gai.get('classificacao') or '').lower()})"
            + (f", porém {gai.get('alerta').lower()}" if gai.get("alerta") else ".")
        )
    if cpi.get("calculado"):
        extras.append(
            f"O CPI foi estimado em {cpi.get('escore_composto')} ({str(cpi.get('classificacao') or '').lower()})."
        )
    if discrepancias:
        extras.append("Foram identificadas discrepâncias clinicamente relevantes entre índices, o que recomenda interpretação cautelosa do perfil global.")
    if facilidades:
        extras.append("Também foram observadas facilidades e fragilidades relativas entre subtestes, sugerindo variabilidade intraindividual relevante.")

    return text + (" " + " ".join(extras) if extras else "")
