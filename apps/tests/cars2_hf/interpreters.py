from .constants import ITEMS

LABELS = {key: label for key, label in ITEMS}


def build_cars2_hf_interpretation(computed_payload: dict, classification: dict) -> str:
    raw_total = computed_payload["raw_total"]
    t_score = computed_payload["t_score"]
    percentile = computed_payload["percentile"]
    severity_group = classification["severity_group"]

    highest = computed_payload["highest_domains"]
    highest_labels = [LABELS.get(item, item) for item in highest]
    highest_text = ", ".join(highest_labels[:-1]) + " e " + highest_labels[-1]
    if len(highest_labels) == 1:
        highest_text = highest_labels[0]

    if classification["severity_code"] == "minimal_or_none":
        caution = (
            "O perfil sugere discreta expressão de sinais compatíveis com o protocolo, "
            "devendo ser interpretado com cautela no contexto clínico."
        )
    elif classification["severity_code"] == "mild_to_moderate":
        caution = (
            "O perfil sugere indicativos compatíveis com alterações leves a moderadas, "
            "com impacto funcional variavel conforme o contexto."
        )
    elif classification["severity_code"] == "severe":
        caution = (
            "O perfil sugere comprometimento importante, com sinais clínicos mais amplos "
            "e necessidade de integracao com a avaliacao global."
        )
    else:
        caution = "O resultado deve ser interpretado a partir da coerência interna do protocolo."

    return (
        f"O CARS2-HF evidenciou escore bruto total de {raw_total}, correspondente a "
        f"T-escore {t_score} e percentil {percentile}. A classificação obtida situa o "
        f"examinando na faixa de {severity_group.lower()}. Observa-se que os indicadores "
        f"mais elevados concentraram-se nos domínios de {highest_text}, sugerindo maior "
        f"comprometimento relativo em aspectos associados à reciprocidade social, "
        f"comunicação e flexibilidade comportamental. {caution}"
    )
