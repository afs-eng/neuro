import json
import os


FACTOR_MAP = {
    "Motivação Social": "motivacao_social",
    "Percepção Social": "percepcao_social",
    "Cognição Social": "cognicao_social",
    "Comunicação Social": "comunicacao_social",
    "Padrões Restritos e Repetitivos": "padroes_restritos",
}

ITENS_INVERTIDOS = {3, 7, 11, 12, 15, 17, 21, 22, 26, 32, 38, 40, 43, 45, 48, 52, 55}


def load_items(form: str) -> tuple[dict, dict]:
    items_file = os.path.join(os.path.dirname(__file__), "items.json")
    with open(items_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    form_key = form if form in data else "idade_escolar"
    items = data.get(form_key, [])

    factor_items: dict = {}
    items_with_desc: dict = {}
    for entry in items:
        item_num = entry["item"]
        fator = entry["fator"]
        factor_key = FACTOR_MAP.get(fator)
        if factor_key:
            if factor_key not in factor_items:
                factor_items[factor_key] = []
            factor_items[factor_key].append(item_num)
            items_with_desc[item_num] = {
                "fator": fator,
                "pergunta": entry.get("pergunta", ""),
            }

    return factor_items, items_with_desc


def convert_response(value, item=None):
    if value is None:
        return 0
    if item and item in ITENS_INVERTIDOS:
        return 4 - value
    return value - 1


def calculate_factor_score(responses: dict, items: list[int]) -> int:
    return sum(responses.get(i, 0) for i in items)


def get_factor_name(factor_key: str) -> str:
    names = {
        "percepcao_social": "Percepção Social",
        "cognicao_social": "Cognição Social",
        "comunicacao_social": "Comunicação Social",
        "motivacao_social": "Motivação Social",
        "padroes_restritos": "Padrões Restritos e Repetitivos",
    }
    return names.get(factor_key, factor_key)


def compute_srs2_scores(raw_responses: dict, form: str) -> dict:
    responses = {}
    for k, v in raw_responses.items():
        try:
            item_num = int(k)
        except (ValueError, TypeError):
            continue
        if v is not None:
            responses[item_num] = convert_response(v, item_num)

    factor_items_dict, _ = load_items(form)

    results = {}
    for factor_key, items in factor_items_dict.items():
        raw_score = calculate_factor_score(responses, items)
        results[factor_key] = {
            "nome": get_factor_name(factor_key),
            "escore": raw_score,
            "max": len(items) * 3,
        }

    cis = (
        results.get("percepcao_social", {}).get("escore", 0)
        + results.get("cognicao_social", {}).get("escore", 0)
        + results.get("comunicacao_social", {}).get("escore", 0)
        + results.get("motivacao_social", {}).get("escore", 0)
    )

    max_cis = (
        results.get("percepcao_social", {}).get("max", 0)
        + results.get("cognicao_social", {}).get("max", 0)
        + results.get("comunicacao_social", {}).get("max", 0)
        + results.get("motivacao_social", {}).get("max", 0)
    )

    results["cis"] = {
        "nome": "Comunicação e Interação Social",
        "escore": cis,
        "max": max_cis,
    }

    total = cis + results.get("padroes_restritos", {}).get("escore", 0)
    results["total"] = {
        "nome": "Pontuação SRS-2 Total",
        "escore": total,
        "max": 65 * 3,
    }

    results["form"] = form

    return results
