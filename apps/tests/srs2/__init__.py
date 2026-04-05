from apps.tests.base.types import BaseTestModule, TestContext
from apps.tests.registry import register_test_module
from .config import SRS2_CODE, SRS2_NAME
from .norms import (
    NORMS,
    get_age_band,
    get_norm_data,
    classify_tscore,
)
from .validators import validate_srs2_input
from typing import Optional
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


class SRS2Module(BaseTestModule):
    code = SRS2_CODE
    name = SRS2_NAME

    def validate(self, context: TestContext) -> list[str]:
        responses = context.raw_scores.get("responses", {})

        errors = []
        for key, value in responses.items():
            if value is not None and value not in [1, 2, 3, 4]:
                errors.append(f"Item {key}: resposta deve ser 1, 2, 3 ou 4")

        if len(responses) < 65:
            errors.append(f"Esperado 65 respostas, recebidas {len(responses)}")

        if not responses:
            errors.append("Nenhuma resposta recebida")

        return errors

    def compute(self, context: TestContext) -> dict:
        raw_responses = context.raw_scores.get("responses", {})
        form = context.raw_scores.get("form", "idade_escolar")

        responses = {}
        for k, v in raw_responses.items():
            try:
                item_num = int(k)
            except (ValueError, TypeError):
                continue
            if v is not None:
                responses[item_num] = convert_response(v, item_num)

        factor_items = load_items(form)
        factor_items_dict, _ = factor_items

        results = {}
        for factor_key, items in factor_items_dict.items():
            raw_score = calculate_factor_score(responses, items)
            results[factor_key] = {
                "nome": self._get_factor_name(factor_key),
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

    def _get_factor_name(self, factor_key: str) -> str:
        names = {
            "percepcao_social": "Percepção Social",
            "cognicao_social": "Cognição Social",
            "comunicacao_social": "Comunicação Social",
            "motivacao_social": "Motivação Social",
            "padroes_restritos": "Padrões Restritos e Repetitivos",
        }
        return names.get(factor_key, factor_key)

    def classify(self, computed_data: dict, **kwargs) -> dict:
        form = computed_data.get("form", "idade_escolar")
        gender = kwargs.get("gender", "M")
        age = kwargs.get("age", 10)

        age_band = get_age_band(age, form)

        results = []

        score_keys = [
            "percepcao_social",
            "cognicao_social",
            "comunicacao_social",
            "motivacao_social",
            "padroes_restritos",
            "cis",
            "total",
        ]

        for key in score_keys:
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

    def interpret(self, context: TestContext, merged_data: dict) -> str:
        results = merged_data.get("resultados", [])
        if not results:
            return "Sem resultados para interpretação."

        lines = []
        lines.append("=" * 95)
        lines.append(
            f"{'Fator':<45} {'Pts Brts':>10} {'T-Score':>10} {'Percentil':>12}  Classificação"
        )
        lines.append("=" * 95)

        for r in results:
            nome = r["nome"][:43] if len(r["nome"]) > 43 else r["nome"]
            bruto = f"{r['bruto']}/{r['max']}"
            tscore_formatted = f"{r['tscore']:.1f}" if r.get("tscore") is not None else "-"
            
            p_val = r.get("percentil")
            if p_val is not None:
                if p_val > 99:
                    percentil = ">99"
                elif p_val < 1:
                    percentil = "<1"
                else:
                    percentil = f"{p_val:.0f}"
            else:
                percentil = "-"
                
            classificacao = r.get("classificacao", "-")

            lines.append(
                f"{nome:<45} {bruto:>10} {tscore_formatted:>10} {percentil:>12}  {classificacao}"
            )

        lines.append("=" * 95)

        return "\n".join(lines)


register_test_module(SRS2_CODE, SRS2Module())
