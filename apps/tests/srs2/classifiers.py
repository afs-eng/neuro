from .norms import classify_tscore, get_age_band, get_norm_data


SCORE_KEYS = [
    "percepcao_social",
    "cognicao_social",
    "comunicacao_social",
    "motivacao_social",
    "padroes_restritos",
    "cis",
    "total",
]


def classify_srs2_scores(computed_data: dict, gender: str = "M", age: int = 10) -> dict:
    form = computed_data.get("form", "idade_escolar")
    age_band = get_age_band(age, form)

    results = []
    for key in SCORE_KEYS:
        score_data = computed_data.get(key, {})
        raw = score_data.get("escore", 0)

        tscore, percentil = get_norm_data(raw, form, gender, key)
        classification = classify_tscore(tscore)

        results.append(
            {
                "variavel": key,
                "nome": score_data.get("nome", key),
                "bruto": raw,
                "max": score_data.get("max", 0),
                "tscore": tscore,
                "percentil": percentil,
                "classificacao": classification,
            }
        )

    return {
        "faixa_etaria": age_band,
        "form": form,
        "resultados": results,
    }
