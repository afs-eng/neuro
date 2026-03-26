from apps.tests.base.types import BaseTestModule, TestContext
from apps.tests.registry import register_test_module
from .calculators import (
    WISC4_CODE,
    WISC4_NAME,
    WISC4_SUBTESTS,
    WISC4_INDICES,
    _carregar_tabela_ncp,
    _calcular_idade,
    _idade_em_meses,
    buscar_ponderado,
    get_classification_padrao,
    get_classification_composto,
    calculate_index_score,
    calculate_qi_total,
    calculate_confidence_interval,
    lookup_composite_score,
    lookup_gai_score,
    lookup_cpi_score,
)
from .classifiers import find_strengths_weaknesses, find_significant_differences
from .interpreters import interpret_index, interpret_qi


class WISC4Module(BaseTestModule):
    code = WISC4_CODE
    name = WISC4_NAME

    def validate(self, context: TestContext) -> list[str]:
        errors = []

        birth_date = context.reviewed_scores.get("birth_date")
        evaluation_date = context.reviewed_scores.get("evaluation_date")
        if birth_date and evaluation_date:
            from datetime import date as dt

            bd = (
                dt.fromisoformat(birth_date)
                if isinstance(birth_date, str)
                else birth_date
            )
            ed = (
                dt.fromisoformat(evaluation_date)
                if isinstance(evaluation_date, str)
                else evaluation_date
            )
            anos, meses = _calcular_idade(bd, ed)
            idade_meses = _idade_em_meses(anos, meses)
            min_meses = _idade_em_meses(6, 0)
            max_meses = _idade_em_meses(16, 11)
            if idade_meses < min_meses or idade_meses > max_meses:
                errors.append(
                    f"WISC-IV é indicado para faixa etária de 6 anos a 16 anos e 11 meses. "
                    f"Paciente com {anos} anos e {meses} meses está fora da faixa."
                )

        for code, config in WISC4_SUBTESTS.items():
            valor = context.raw_scores.get(code)
            if valor is None:
                errors.append(f"Subteste '{config['name']}' não informado")
            elif valor < 0:
                errors.append(f"{config['name']}: escore bruto não pode ser negativo")
            elif valor > config["max"]:
                errors.append(
                    f"{config['name']}: escore bruto ({valor}) maior que o máximo ({config['max']})"
                )
        return errors

    def compute(self, context: TestContext) -> dict:
        patient_name = context.patient_name
        birth_date = context.reviewed_scores.get("birth_date")
        evaluation_date = context.reviewed_scores.get("evaluation_date")

        if birth_date and evaluation_date:
            from datetime import date

            if isinstance(birth_date, str):
                birth_date = date.fromisoformat(birth_date)
            if isinstance(evaluation_date, str):
                evaluation_date = date.fromisoformat(evaluation_date)
            anos, meses = _calcular_idade(birth_date, evaluation_date)
        else:
            anos, meses = 6, 0

        tabela = _carregar_tabela_ncp(anos, meses)

        subtest_results = {}
        for code, config in WISC4_SUBTESTS.items():
            eb = context.raw_scores.get(code, 0)
            coluna = config["code"]
            try:
                pp = buscar_ponderado(tabela, coluna, eb)
            except ValueError:
                pp = 10
            classificacao = get_classification_padrao(pp)
            ic = calculate_confidence_interval(pp, sem=2.0)

            subtest_results[code] = {
                "subteste": config["name"],
                "codigo": config["code"],
                "escore_bruto": eb,
                "escore_padrao": pp,
                "percentil": 50,
                "classificacao": classificacao,
                "intervalo_confianca_95": ic,
            }

        return subtest_results

    def classify(self, computed_data: dict, faixa: str = "") -> dict:
        confidence_level = faixa if faixa in ("90", "95") else "95"

        index_results = []
        for idx_code, idx_config in WISC4_INDICES.items():
            sp_list = [
                computed_data[code]["escore_padrao"]
                for code in idx_config["subtests"]
                if code in computed_data
            ]
            soma_ponderados = calculate_index_score(sp_list)

            composite_data = None
            if idx_code in ("icv", "iop", "imt", "ivp"):
                try:
                    composite_data = lookup_composite_score(idx_code, soma_ponderados)
                except ValueError:
                    composite_data = {
                        "escore": 0,
                        "percentil": 0,
                        "ic_90": (0, 0),
                        "ic_95": (0, 0),
                    }

            subtests_for_index = [
                computed_data[code]
                for code in idx_config["subtests"]
                if code in computed_data
            ]

            index_entry = {
                "indice": idx_code,
                "nome": idx_config["name"],
                "soma_ponderados": soma_ponderados,
                "subtestes": subtests_for_index,
            }
            if composite_data:
                index_entry.update(
                    {
                        "escore_composto": composite_data["escore"],
                        "percentil": composite_data["percentil"],
                        "intervalo_confianca": composite_data[f"ic_{confidence_level}"],
                    }
                )
            index_results.append(index_entry)

        somas_ponderados = [r["soma_ponderados"] for r in index_results]
        soma_total = sum(somas_ponderados)

        qit_data = None
        try:
            qit_data = lookup_composite_score("qit", soma_total)
        except ValueError:
            qit_data = {
                "escore": calculate_qi_total(somas_ponderados),
                "percentil": 0,
                "ic_90": (0, 0),
                "ic_95": (0, 0),
            }

        qi_total = qit_data["escore"]

        # GAI = ICV + IOP
        gai_soma = sum(
            r["soma_ponderados"] for r in index_results if r["indice"] in ("icv", "iop")
        )
        gai_data = None
        try:
            gai_data = lookup_gai_score(gai_soma)
        except ValueError:
            gai_data = {
                "escore": 0,
                "percentil": 0,
                "ic_95": (0, 0),
                "classificacao": "",
            }

        # CPI = IMO + IVP
        cpi_soma = sum(
            r["soma_ponderados"] for r in index_results if r["indice"] in ("imt", "ivp")
        )
        cpi_data = None
        try:
            cpi_data = lookup_cpi_score(cpi_soma)
        except ValueError:
            cpi_data = {
                "escore": 0,
                "percentil": 0,
                "ic_95": (0, 0),
                "classificacao": "",
            }

        all_subtests = list(computed_data.values())
        pontos_fortes, pontos_fragilizados = find_strengths_weaknesses(all_subtests)
        diferencas = find_significant_differences(index_results, qi_total)

        return {
            "subtestes": all_subtests,
            "indices": index_results,
            "qi_total": qi_total,
            "qit_data": {
                "soma_ponderados": soma_total,
                "escore_composto": qit_data["escore"],
                "percentil": qit_data["percentil"],
                "intervalo_confianca": qit_data[f"ic_{confidence_level}"],
            },
            "gai_data": {
                "soma_ponderados": gai_soma,
                "escore_composto": gai_data["escore"],
                "percentil": gai_data["percentil"],
                "intervalo_confianca": gai_data["ic_95"],
                "classificacao": gai_data["classificacao"],
            },
            "cpi_data": {
                "soma_ponderados": cpi_soma,
                "escore_composto": cpi_data["escore"],
                "percentil": cpi_data["percentil"],
                "intervalo_confianca": cpi_data["ic_95"],
                "classificacao": cpi_data["classificacao"],
            },
            "pontos_fortes": pontos_fortes,
            "pontos_fragilizados": pontos_fragilizados,
            "diferencas_significativas": diferencas,
            "confidence_level": confidence_level,
        }

    def interpret(self, context: TestContext, merged_data: dict) -> str:
        parts = []
        parts.append(f"QI Total: {merged_data['qi_total']}")
        parts.append("")

        for idx in merged_data.get("indices", []):
            parts.append(f"{idx['nome']}: {idx['soma_ponderados']}")
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
