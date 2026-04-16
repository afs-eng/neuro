def classify_cars2_hf(raw_total: float) -> dict:
    if 15 <= raw_total <= 27.5:
        return {
            "severity_group": "Sintomas mínimos ou inexistentes do transtorno do espectro do autismo",
            "severity_code": "minimal_or_none",
        }

    if 28 <= raw_total <= 33.5:
        return {
            "severity_group": "Leve a moderado sintomas do transtorno do espectro do autismo",
            "severity_code": "mild_to_moderate",
        }

    if raw_total >= 34:
        return {
            "severity_group": "Sintomas severos do transtorno do espectro do autismo",
            "severity_code": "severe",
        }

    return {"severity_group": "Resultado inválido", "severity_code": "invalid"}
