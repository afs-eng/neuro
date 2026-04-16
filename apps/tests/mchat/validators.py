from .constants import ITEMS, VALID_RESPONSES


def normalize_answer(value) -> str:
    if value in (1, "1", True, "Sim", "sim"):
        return "1"
    if value in (0, "0", False, "Não", "nao", "não"):
        return "0"
    return str(value)


def validate_mchat_payload(payload: dict) -> None:
    if "items" not in payload:
        raise ValueError("O campo 'items' é obrigatório.")

    expected_keys = {slug for _, slug in ITEMS}
    received_keys = set(payload["items"].keys())

    missing = expected_keys - received_keys
    extra = received_keys - expected_keys

    if missing:
        raise ValueError(f"Itens obrigatórios ausentes: {sorted(missing)}")

    if extra:
        raise ValueError(f"Itens desconhecidos enviados: {sorted(extra)}")

    for key, item in payload["items"].items():
        answer = normalize_answer(item.get("answer"))
        if answer not in VALID_RESPONSES:
            raise ValueError(
                f"Resposta inválida para '{key}'. Valores permitidos: {VALID_RESPONSES}"
            )
