from apps.tests.base.types import BaseTestModule, TestContext
from apps.tests.registry import register_test_module

from .calculators import compute_bfp_scores
from .config import BFP_CODE, BFP_NAME
from .interpreters import get_report_interpretation
from .schemas import BFPRawInput
from .validators import validate_bfp_input


class BFPModule(BaseTestModule):
    code = BFP_CODE
    name = BFP_NAME

    def validate(self, context: TestContext) -> list[str]:
        try:
            BFPRawInput(**context.raw_scores)
        except Exception as e:
            return [f"Erro na validação: {e}"]
        return validate_bfp_input(context.raw_scores)

    def compute(self, context: TestContext) -> dict:
        return compute_bfp_scores(context.raw_scores)

    def classify(self, computed_data: dict, **kwargs) -> dict:
        factor_classifications = {
            code: result["classification"]
            for code, result in computed_data.get("factors", {}).items()
        }
        facet_classifications = {
            code: result["classification"]
            for code, result in computed_data.get("facets", {}).items()
        }
        highlights = [
            {
                "code": code,
                "name": result["name"],
                "classification": result["classification"],
                "percentile": result["percentile"],
            }
            for code, result in computed_data.get("facets", {}).items()
            if result["classification"] != "Médio"
        ]
        return {
            "sample": computed_data.get("sample", "geral"),
            "factor_classifications": factor_classifications,
            "facet_classifications": facet_classifications,
            "highlights": highlights,
        }

    def interpret(self, context: TestContext, merged_data: dict) -> str:
        return get_report_interpretation(merged_data, patient_name=context.patient_name)


register_test_module(BFP_CODE, BFPModule())
