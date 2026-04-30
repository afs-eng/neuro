from __future__ import annotations

from .calculators import extract_bfp_responses, normalize_sample
from .config import SAMPLE_LABELS


def validate_bfp_input(raw_payload: dict) -> list[str]:
    errors = []
    sample = normalize_sample(
        raw_payload.get("sample") or raw_payload.get("amostra") or raw_payload.get("norm_group")
    )
    if sample not in SAMPLE_LABELS:
        errors.append("Amostra normativa do BFP inválida. Use geral, masculino ou feminino.")

    responses = extract_bfp_responses(raw_payload)
    for item in range(1, 127):
        score = responses.get(item)
        if score is None:
            errors.append(f"Item {item} não respondido.")
            continue
        if score < 1 or score > 7:
            errors.append(f"Item {item} possui valor inválido ({score}).")

    return errors
