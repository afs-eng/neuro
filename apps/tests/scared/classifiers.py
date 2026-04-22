from .config import CHILD_MAX_AGE, FATORES_ANALISE, PAIS_MAXIMOS
from .norms import AUTORRELATO_NORMAS, PAIS_CORTES, normal_cdf, percentil_para_classificacao


def classify_scared_scores(computed_data: dict, idade: int = 0) -> dict:
    form = computed_data.get("form", "child")
    brutos = computed_data.get("brutos", {})
    gender = computed_data.get("gender", "M").lower()
    sexo = "masculino" if gender.startswith("m") else "feminino"

    idade = computed_data.get("age", idade)
    grupo = "crianca" if idade <= CHILD_MAX_AGE else "adolescente"

    linhas = []

    if form == "parent":
        for fator in FATORES_ANALISE:
            bruto = brutos.get(fator, 0)
            maximo = PAIS_MAXIMOS.get(fator, 1)
            corte = PAIS_CORTES.get(fator, 0)
            percentual = round((bruto * 100) / maximo, 2)
            classificacao = "Clínico" if bruto >= corte else "Não clínico"
            linhas.append(
                {
                    "fator": fator,
                    "escore_bruto": bruto,
                    "percentual": percentual,
                    "nota_corte": corte,
                    "classificacao": classificacao,
                }
            )
    else:
        normas_grupo = AUTORRELATO_NORMAS.get(grupo, AUTORRELATO_NORMAS["crianca"])[sexo]
        for fator in FATORES_ANALISE:
            bruto = brutos.get(fator, 0)
            norma = normas_grupo.get(fator, {"media": 0, "dp": 1})
            media = norma["media"]
            dp = norma["dp"]
            z = (bruto - media) / dp if dp > 0 else 0
            percentil = round(normal_cdf(z) * 100, 2)
            classificacao = percentil_para_classificacao(percentil)
            linhas.append(
                {
                    "fator": fator,
                    "escore_bruto": bruto,
                    "media": round(media, 2),
                    "dp": round(dp, 2),
                    "z_score": round(z, 2),
                    "percentil": percentil,
                    "classificacao": classificacao,
                }
            )

    if form == "parent":
        total_bruto = brutos.get("total", 0)
        if total_bruto >= PAIS_CORTES["total"]:
            sintese = "Os resultados sugerem rastreio positivo para sintomas ansiosos clinicamente relevantes."
        else:
            sintese = "Os resultados não atingiram o ponto de corte total para rastreio clínico global."
    else:
        total_perc = next((l["percentil"] for l in linhas if l["fator"] == "total"), 0)
        if total_perc >= 75:
            sintese = "O autorrelato sugere elevação global de sintomas ansiosos em relação à amostra normativa."
        else:
            sintese = "O autorrelato não sugere elevação global importante em relação à amostra normativa."

    return {
        "form_type": form,
        "grupo_etario": grupo,
        "sexo": sexo,
        "analise_geral": linhas,
        "sintese": sintese,
    }
