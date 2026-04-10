from apps.tests.base.types import BaseTestModule, TestContext
from apps.tests.registry import register_test_module
from .config import (
    SCARED_CODE,
    SCARED_NAME,
    FATORES,
    FATORES_TOTAL,
    PAIS_MAXIMOS,
    CHILD_MAX_AGE,
)
from .norms import (
    PAIS_CORTES,
    AUTORRELATO_NORMAS,
    normal_cdf,
    percentil_para_classificacao,
)


class SCAREDModule(BaseTestModule):
    code = SCARED_CODE
    name = SCARED_NAME

    def validate(self, context: TestContext) -> list[str]:
        errors = []
        raw_payload = context.raw_scores
        responses = raw_payload.get("responses", {})

        if not responses:
            errors.append("Nenhuma resposta informada.")

        # Check if all 41 items are present
        for i in range(1, 42):
            val = responses.get(str(i))
            if val is None:
                errors.append(f"Item {i} não respondido.")
            elif val not in [0, 1, 2]:
                errors.append(f"Item {i} possui valor inválido ({val}).")

        return errors

    def compute(self, context: TestContext) -> dict:
        raw_payload = context.raw_scores
        responses = raw_payload.get("responses", {})
        form = raw_payload.get("form", "child")  # 'child' (autorrelato) or 'parent'

        # Convert keys to int for easier factor summing
        resp_int = {int(k): int(v) for k, v in responses.items()}

        brutos = {}
        for fator, itens in FATORES.items():
            brutos[fator] = sum(resp_int.get(i, 0) for i in itens)

        brutos["total"] = sum(resp_int.get(i, 0) for i in FATORES_TOTAL)

        return {
            "form": form,
            "brutos": brutos,
            "gender": raw_payload.get("gender", "M"),
            "age": raw_payload.get("age", context.patient_age),
        }

    def classify(self, computed_data: dict, idade: int = 0) -> dict:
        form = computed_data.get("form", "child")
        brutos = computed_data.get("brutos", {})
        gender = computed_data.get("gender", "M").lower()
        if gender.startswith("m"):
            sexo = "masculino"
        else:
            sexo = "feminino"

        idade = computed_data.get("age", idade)
        grupo = "crianca" if idade <= CHILD_MAX_AGE else "adolescente"

        linhas = []

        if form == "parent":
            # Parent logic (Cutoffs)
            for fator in [
                "panico_sintomas_somaticos",
                "ansiedade_generalizada",
                "ansiedade_separacao",
                "fobia_social",
                "evitacao_escolar",
                "total",
            ]:
                bruto = brutos.get(fator, 0)
                maximo = PAIS_MAXIMOS.get(fator, 1)
                corte = PAIS_CORTES.get(fator, 0)
                percentual = round((bruto * 100) / maximo, 2)
                classificacao = "Clínico" if bruto >= corte else "Não clínico"
                linhas.append(
                    {
                        "fator": fator,
                        "escore_bruto": bruto,
                        "percentual": percentual,
                        "nota_corte": corte,
                        "classificacao": classificacao,
                    }
                )
        else:
            # Self-report logic (Norms/Z-score)
            normas_grupo = AUTORRELATO_NORMAS.get(grupo, AUTORRELATO_NORMAS["crianca"])[
                sexo
            ]
            for fator in [
                "panico_sintomas_somaticos",
                "ansiedade_generalizada",
                "ansiedade_separacao",
                "fobia_social",
                "evitacao_escolar",
                "total",
            ]:
                bruto = brutos.get(fator, 0)
                norma = normas_grupo.get(fator, {"media": 0, "dp": 1})
                media = norma["media"]
                dp = norma["dp"]
                z = (bruto - media) / dp if dp > 0 else 0
                percentil = round(normal_cdf(z) * 100, 2)
                classificacao = percentil_para_classificacao(percentil)
                linhas.append(
                    {
                        "fator": fator,
                        "escore_bruto": bruto,
                        "media": round(media, 2),
                        "dp": round(dp, 2),
                        "z_score": round(z, 2),
                        "percentil": percentil,
                        "classificacao": classificacao,
                    }
                )

        # Integrated synthesis
        if form == "parent":
            total_bruto = brutos.get("total", 0)
            if total_bruto >= PAIS_CORTES["total"]:
                sintese = "Os resultados sugerem rastreio positivo para sintomas ansiosos clinicamente relevantes."
            else:
                sintese = "Os resultados não atingiram o ponto de corte total para rastreio clínico global."
        else:
            total_perc = next(
                (l["percentil"] for l in linhas if l["fator"] == "total"), 0
            )
            if total_perc >= 75:
                sintese = "O autorrelato sugere elevação global de sintomas ansiosos em relação à amostra normativa."
            else:
                sintese = "O autorrelato não sugere elevação global importante em relação à amostra normativa."

        return {
            "form_type": form,
            "grupo_etario": grupo,
            "sexo": sexo,
            "analise_geral": linhas,
            "sintese": sintese,
        }

    def interpret(self, context: TestContext, merged_data: dict) -> str:
        sintese = merged_data.get("sintese", "")
        form_name = (
            "Pais/Cuidadores" if merged_data.get("form_type") == "parent" else "Autorrelato"
        )
        parts = [f"SCARED - {form_name}", "", sintese, ""]

        for linha in merged_data.get("analise_geral", []):
            f = linha["fator"].replace("_", " ").title()
            c = linha["classificacao"]
            e = linha["escore_bruto"]
            parts.append(f"- {f}: {e} ({c})")

        return "\n".join(parts)


register_test_module(SCARED_CODE, SCAREDModule())
