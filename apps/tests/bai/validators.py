from __future__ import annotations

from .constants import ITEMS
from .schemas import BAIRawInput, BAIRawPayload


class BAIValidationError(Exception):
    pass


def validate_bai_input(data: BAIRawInput) -> list[str]:
    """Valida input do BAI para uso via API (Django Ninja)."""
    erros = []
    for i in range(1, 22):
        key = f"item_{i:02d}"
        if not hasattr(data, key):
            erros.append(f"Item {i} ausente")
        elif getattr(data, key) not in (0, 1, 2, 3):
            erros.append(f"Item {i} deve ser 0, 1, 2 ou 3")
    return erros


class BAIValidator:
    """Validador para uso interno do módulo BAI."""

    @staticmethod
    def validate(payload: BAIRawPayload) -> None:
        if not payload.responses:
            raise BAIValidationError("O BAI exige respostas para os 21 itens.")

        item_numbers = [item.item_number for item in payload.responses]
        if len(set(item_numbers)) != len(item_numbers):
            raise BAIValidationError("Há itens duplicados no payload do BAI.")

        valid_numbers = set(range(1, len(ITEMS) + 1))
        invalid_numbers = sorted(set(item_numbers) - valid_numbers)
        if invalid_numbers:
            raise BAIValidationError(f"Itens inválidos encontrados: {invalid_numbers}")

        for item in payload.responses:
            if item.score not in (0, 1, 2, 3):
                raise BAIValidationError(
                    f"O item {item.item_number} possui valor inválido: {item.score}. Use apenas 0, 1, 2 ou 3."
                )
