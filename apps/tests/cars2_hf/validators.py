from .constants import ITEMS, VALID_SCORES


def validate_cars2_hf_payload(payload: dict) -> None:
    if "items" not in payload:
        raise ValueError("O campo 'items' e obrigatorio.")

    expected_keys = {key for key, _ in ITEMS}
    received_keys = set(payload["items"].keys())

    missing = expected_keys - received_keys
    extra = received_keys - expected_keys

    if missing:
        raise ValueError(f"Itens obrigatorios ausentes: {sorted(missing)}")

    if extra:
        raise ValueError(f"Itens desconhecidos enviados: {sorted(extra)}")

    for key, item in payload["items"].items():
        score = item.get("score")
        if score not in VALID_SCORES:
            raise ValueError(
                f"Pontuacao invalida para '{key}'. Valores permitidos: {VALID_SCORES}"
            )
