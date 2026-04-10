"""
Exemplo de integração com Django.

A ideia é:
1. buscar Evaluation, Patient, Anamnesis e TestApplication no ORM
2. converter para EvaluationContext
3. gerar ReportDraft
4. salvar em models Report e ReportSection
"""

from __future__ import annotations

from dataclasses import asdict

from laudo_ai.context_builder import EvaluationContextBuilder
from laudo_ai.section_generators import ReportGenerator


def generate_report_from_django(evaluation_payload: dict) -> dict:
    builder = EvaluationContextBuilder()
    context = builder.from_dict(evaluation_payload)

    generator = ReportGenerator()
    draft = generator.generate_draft(context)

    return {
        "model_name": draft.model_name,
        "generated_context": asdict(context),
        "compiled_text": draft.compile_text(),
        "sections": [
            {
                "key": section.key.value,
                "title": section.title,
                "text": section.text,
                "generated_by": section.generated_by,
            }
            for section in draft.sections
        ],
    }
