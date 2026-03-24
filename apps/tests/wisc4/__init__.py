from apps.tests.base.types import BaseTestModule, TestContext
from apps.tests.registry import register_test_module
from .config import WISC4_CODE, WISC4_NAME, WISC4_SUBTESTS, WISC4_INDICES, IndexCode
from .schemas import WISC4RawInput, SubtestResult, IndexResult
from .validators import validate_wisc4_input
from .calculators import (
    convert_raw_to_standard,
    get_classification,
    calculate_index_score,
    calculate_qi_total,
    classify_index,
    classify_qi,
    calculate_confidence_interval,
)
from .classifiers import find_strengths_weaknesses, find_significant_differences
from .interpreters import interpret_index, interpret_qi


class WISC4Module(BaseTestModule):
    code = WISC4_CODE
    name = WISC4_NAME

    def validate(self, context: TestContext) -> list[str]:
        try:
            data = WISC4RawInput(**context.raw_scores)
            return validate_wisc4_input(data)
        except Exception as e:
            return [f"Erro na validação: {e}"]

    def compute(self, context: TestContext) -> dict:
        data = WISC4RawInput(**context.raw_scores)
        raw_dict = data.model_dump()

        subtest_results = {}
        for code, config in WISC4_SUBTESTS.items():
            eb = raw_dict[code]["escore_bruto"]
            escore_padrao, percentil = convert_raw_to_standard(code, eb)
            classificacao = get_classification(escore_padrao)
            ic = calculate_confidence_interval(escore_padrao, sem=2.0)

            subtest_results[code] = {
                "subteste": config.name,
                "escore_bruto": eb,
                "escore_padrao": escore_padrao,
                "percentil": percentil,
                "classificacao": classificacao,
                "intervalo_confianca_95": ic,
            }

        return subtest_results

    def classify(self, computed_data: dict) -> dict:
        index_results = []

        for idx_code, idx_config in WISC4_INDICES.items():
            sp_list = [
                computed_data[code]["escore_padrao"]
                for code in idx_config.subtests
                if code in computed_data
            ]
            escore_composto = calculate_index_score(sp_list)
            percentil, classificacao = classify_index(escore_composto)
            ic = calculate_confidence_interval(escore_composto, sem=3.0)

            subtests_for_index = [
                computed_data[code]
                for code in idx_config.subtests
                if code in computed_data
            ]

            index_results.append(
                {
                    "indice": idx_code,
                    "nome": idx_config.name,
                    "escore_composto": escore_composto,
                    "percentil": percentil,
                    "classificacao": classificacao,
                    "subtestes": subtests_for_index,
                    "intervalo_confianca_95": ic,
                }
            )

        escores_compostos = [r["escore_composto"] for r in index_results]
        qi_total = calculate_qi_total(escores_compostos)
        percentil_qi, classificacao_qi = classify_qi(qi_total)
        ic_qi = calculate_confidence_interval(qi_total, sem=3.0)

        all_subtests = list(computed_data.values())
        pontos_fortes, pontos_fragilizados = find_strengths_weaknesses(all_subtests)
        diferencas = find_significant_differences(index_results, qi_total)

        return {
            "subtestes": all_subtests,
            "indices": index_results,
            "qi_total": qi_total,
            "percentil_qi": percentil_qi,
            "classificacao_qi": classificacao_qi,
            "intervalo_confianca_95": ic_qi,
            "pontos_fortes": pontos_fortes,
            "pontos_fragilizados": pontos_fragilizados,
            "diferencas_significativas": diferencas,
        }

    def interpret(self, context: TestContext, merged_data: dict) -> str:
        parts = []
        parts.append(
            f"QI Total: {merged_data['qi_total']} ({merged_data['classificacao_qi']})"
        )
        parts.append(interpret_qi(merged_data["classificacao_qi"]))
        parts.append("")

        for idx in merged_data.get("indices", []):
            interp = interpret_index(idx["indice"], idx["classificacao"])
            parts.append(
                f"{idx['nome']}: {idx['escore_composto']} ({idx['classificacao']})"
            )
            parts.append(interp)
            parts.append("")

        if merged_data.get("pontos_fortes"):
            parts.append(f"Pontos fortes: {', '.join(merged_data['pontos_fortes'])}")
        if merged_data.get("pontos_fragilizados"):
            parts.append(
                f"Pontos fragilizados: {', '.join(merged_data['pontos_fragilizados'])}"
            )
        if merged_data.get("diferencas_significativas"):
            parts.append("Diferenças significativas:")
            parts.extend(merged_data["diferencas_significativas"])

        return "\n".join(parts)


register_test_module(WISC4_CODE, WISC4Module())
