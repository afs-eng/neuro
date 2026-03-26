from apps.tests.base.types import BaseTestModule, TestContext
from apps.tests.registry import register_test_module
from .config import EBADEPIJ_CODE, EBADEPIJ_NAME, ITENS_POSITIVOS, ITENS_NEGATIVOS
from .schemas import EBADEPIJRawInput, EBADEPIJResult, EBADEPIJNorms, ItemDetail
from .validators import validate_ebadep_ij_input
from .calculators import calcular_pontuacoes, classificar_tabela_18, obter_normas
from .interpreters import interpret_result, get_synthesis, get_report_interpretation


class EBADEPIJModule(BaseTestModule):
    code = EBADEPIJ_CODE
    name = EBADEPIJ_NAME

    def validate(self, context: TestContext) -> list[str]:
        try:
            data = EBADEPIJRawInput(**context.raw_scores)
            return validate_ebadep_ij_input(data)
        except Exception as e:
            return [f"Erro na validação: {e}"]

    def compute(self, context: TestContext) -> dict:
        respostas = []
        for i in range(1, 28):
            key = f"item_{i:02d}"
            respostas.append(context.raw_scores[key])
        return calcular_pontuacoes(respostas)

    def classify(self, computed_data: dict, faixa: str = "") -> dict:
        pontuacao_total = computed_data["pontuacao_total"]
        classificacao = classificar_tabela_18(pontuacao_total)
        normas = obter_normas(pontuacao_total)

        detalhe_itens = []
        for d in computed_data.get("detalhe_itens", []):
            detalhe_itens.append(ItemDetail(**d))

        result = EBADEPIJResult(
            soma_itens_negativos=computed_data["soma_itens_negativos"],
            soma_itens_positivos=computed_data["soma_itens_positivos"],
            pontuacao_total=pontuacao_total,
            classificacao=classificacao,
            normas=EBADEPIJNorms(**normas) if normas else None,
            detalhe_itens=detalhe_itens,
        )

        items_criticos = [d for d in detalhe_itens if d.corrigido == 2]

        return {
            "result": result.model_dump(),
            "classificacao": classificacao,
            "pontuacao_total": pontuacao_total,
            "normas": normas,
            "items_criticos": [d.model_dump() for d in items_criticos],
            "sintese": get_synthesis(classificacao),
        }

    def interpret(self, context: TestContext, merged_data: dict) -> str:
        classificacao = merged_data.get("classificacao", "")
        interp = interpret_result(classificacao)

        parts = []
        parts.append(f"Classificação: {classificacao}")
        parts.append(f"Interpretação: {interp.get('geral', '')}")

        if merged_data.get("items_criticos"):
            items = [str(d["item"]) for d in merged_data["items_criticos"]]
            parts.append(
                f"Itens com escore máximo (pontuação 2 corrigido): {', '.join(items)}"
            )

        parts.append(f"Síntese: {get_synthesis(classificacao)}")

        return "\n".join(parts)


register_test_module(EBADEPIJ_CODE, EBADEPIJModule())
