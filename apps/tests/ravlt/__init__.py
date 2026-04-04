from apps.tests.base.types import BaseTestModule, TestContext
from apps.tests.registry import register_test_module
from .config import (
    RAVLT_CODE,
    RAVLT_NAME,
    RAVLT_TRIAL_FIELDS,
    RAVLT_MAX_SCORES,
)
from .norms import (
    NORMS,
    get_age_band,
    safe_div,
    compute_recognition_score,
    z_score,
    calc_weighted_score,
    percentile_from_z,
    classify_by_percentile,
)
from datetime import date


class RAVLTModule(BaseTestModule):
    code = RAVLT_CODE
    name = RAVLT_NAME

    def validate(self, context: TestContext) -> list[str]:
        errors = []

        for field, label in RAVLT_TRIAL_FIELDS.items():
            valor = context.raw_scores.get(field)
            if valor is None:
                errors.append(f"'{label}' não informado")
            elif valor < 0:
                errors.append(f"{label}: escore não pode ser negativo")
            elif valor > RAVLT_MAX_SCORES.get(field, 15):
                errors.append(
                    f"{label}: escore ({valor}) maior que o máximo ({RAVLT_MAX_SCORES.get(field, 15)})"
                )

        reconhecimento = context.raw_scores.get("reconhecimento", 0)
        if reconhecimento is not None and (reconhecimento < 0 or reconhecimento > 50):
            errors.append("Reconhecimento deve estar entre 0 e 50")

        return errors

    def compute(self, context: TestContext) -> dict:
        a1 = context.raw_scores.get("a1", 0)
        a2 = context.raw_scores.get("a2", 0)
        a3 = context.raw_scores.get("a3", 0)
        a4 = context.raw_scores.get("a4", 0)
        a5 = context.raw_scores.get("a5", 0)
        b = context.raw_scores.get("b", 0)
        a6 = context.raw_scores.get("a6", 0)
        a7 = context.raw_scores.get("a7", 0)
        reconhecimento = context.raw_scores.get("reconhecimento", 0)

        rec_lista_a = compute_recognition_score(reconhecimento)
        escore_total = a1 + a2 + a3 + a4 + a5
        alt = escore_total - (5 * a1)
        ve = safe_div(a7, a6) if a6 else None
        ip = safe_div(b, a1) if a1 else None
        ir = safe_div(a6, a5) if a5 else None

        results = {}
        for field, label in RAVLT_TRIAL_FIELDS.items():
            valor = context.raw_scores.get(field, 0)
            results[field] = {
                "campo": label,
                "escore": valor,
                "max": RAVLT_MAX_SCORES.get(field, 15),
            }

        results["reconhecimento"] = {
            "campo": "Reconhecimento Lista A",
            "escore": rec_lista_a,
            "max": 15,
        }
        results["escore_total"] = {
            "campo": "Escore Total",
            "escore": escore_total,
            "max": 75,
        }
        results["aprend_longo"] = {
            "campo": "Aprend. longo das Tentativas",
            "escore": alt,
            "max": 60,
        }
        results["velocidade_esquecimento"] = {
            "campo": "Velocidade de Esquecimento",
            "escore": ve,
        }
        results["interferencia_proativa"] = {
            "campo": "Interferência Proativa",
            "escore": ip,
        }
        results["interferencia_retroativa"] = {
            "campo": "Interferência Retroativa",
            "escore": ir,
        }

        return results

    def classify(self, computed_data: dict, idade: int = 25) -> dict:
        try:
            band = get_age_band(idade)
        except ValueError:
            band = "21-30"

        norms = NORMS.get(band, NORMS["21-30"])

        results = []
        for var_name in [
            "A1",
            "A2",
            "A3",
            "A4",
            "A5",
            "B1",
            "A6",
            "A7",
            "Reconhecimento Lista A",
            "Escore Total",
            "Aprend. longo das Tentativas",
            "Velocidade de Esquecimento",
            "Interferência Proativa",
            "Interferência Retroativa",
        ]:
            raw = None
            key_map = {
                "A1": "a1",
                "A2": "a2",
                "A3": "a3",
                "A4": "a4",
                "A5": "a5",
                "B1": "b",
                "A6": "a6",
                "A7": "a7",
            }
            if var_name in key_map:
                raw = computed_data.get(key_map[var_name], {}).get("escore", 0)
            elif var_name == "Reconhecimento Lista A":
                raw = computed_data.get("reconhecimento", {}).get("escore", 0)
            elif var_name == "Escore Total":
                raw = computed_data.get("escore_total", {}).get("escore", 0)
            elif var_name == "Aprend. longo das Tentativas":
                raw = computed_data.get("aprend_longo", {}).get("escore", 0)
            elif var_name == "Velocidade de Esquecimento":
                raw = computed_data.get("velocidade_esquecimento", {}).get("escore")
            elif var_name == "Interferência Proativa":
                raw = computed_data.get("interferencia_proativa", {}).get("escore")
            elif var_name == "Interferência Retroativa":
                raw = computed_data.get("interferencia_retroativa", {}).get("escore")

            norm = norms.get(var_name)
            z = z_score(raw, norm.mean, norm.sd) if norm and raw is not None else None
            weighted = calc_weighted_score(z)
            percentile = percentile_from_z(z)
            classification = classify_by_percentile(percentile)

            results.append(
                {
                    "variavel": var_name,
                    "bruto": raw,
                    "media": norm.mean if norm else None,
                    "dp": norm.sd if norm else None,
                    "z": z,
                    "ponderado": weighted,
                    "percentil": percentile,
                    "classificacao": classification,
                }
            )

        return {
            "faixa_etaria": band,
            "idade": idade,
            "resultados": results,
        }

    def interpret(self, context: TestContext, merged_data: dict) -> str:
        results = merged_data.get("resultados", [])
        if not results:
            return "Sem resultados para interpretação."

        parts = []
        parts.append(
            f"RAVLT - Resultados | Faixa etária: {merged_data.get('faixa_etaria', '-')}"
        )
        parts.append("")

        for r in results:
            if r.get("bruto") is not None:
                parts.append(f"{r['variavel']}: {r['bruto']} ({r['classificacao']})")

        return "\n".join(parts)


register_test_module(RAVLT_CODE, RAVLTModule())
