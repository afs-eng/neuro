from __future__ import annotations

from typing import Iterable, List

from .bibliography import DEFAULT_REFERENCES
from .schemas import (
    ClinicalHistory,
    EvaluationContext,
    PatientInfo,
    ReferralInfo,
    SessionInfo,
    StyleRules,
    TestResult,
)


class EvaluationContextBuilder:
    """
    Builder para transformar dados vindos do Django ORM, serializers ou APIs internas
    em um contexto estruturado e estável para geração do laudo.
    """

    def from_dict(self, data: dict) -> EvaluationContext:
        tests: List[TestResult] = [
            TestResult(**item) for item in data.get("tests", [])
        ]

        references = data.get("references") or DEFAULT_REFERENCES

        return EvaluationContext(
            author_name=data["author_name"],
            author_registry=data["author_registry"],
            patient=PatientInfo(**data["patient"]),
            referral=ReferralInfo(**data["referral"]),
            sessions=SessionInfo(**data.get("sessions", {})),
            tests=tests,
            history=ClinicalHistory(**data["history"]),
            style_rules=StyleRules(**data.get("style_rules", {})),
            references=references,
            report_date_city=data.get("report_date_city", "Goiânia"),
            report_date_text=data.get("report_date_text", ""),
            model_name=data.get("model_name", "laudo_neuropsicologico_padrao"),
        )

    def summarize_tests(self, tests: Iterable[TestResult]) -> str:
        names = [test.instrument for test in tests if test.applied]
        return "; ".join(names)
