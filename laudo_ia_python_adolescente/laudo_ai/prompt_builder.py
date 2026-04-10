from __future__ import annotations

import json
from dataclasses import asdict
from typing import Dict, Any

from .schemas import EvaluationContext


class PromptBuilder:
    """
    Gera prompts por seção. A IA deve receber um contexto clínico controlado,
    nunca um dump aleatório do banco.
    """

    SYSTEM_RULES = """Você redige seções de laudo neuropsicológico.
Use apenas os dados fornecidos.
Não invente resultados, testes, diagnósticos ou histórico.
Mantenha linguagem técnica, coesa e clínica.
Quando houver indícios, utilize a expressão "hipótese diagnóstica".
Respeite o modelo de laudo institucional."""

    def build_section_prompt(self, section_name: str, context: EvaluationContext) -> str:
        safe_context: Dict[str, Any] = asdict(context)
        return f"""{self.SYSTEM_RULES}

SEÇÃO A GERAR:
{section_name}

CONTEXTO ESTRUTURADO:
{json.dumps(safe_context, ensure_ascii=False, indent=2)}
"""
