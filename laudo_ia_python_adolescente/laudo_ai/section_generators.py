
from __future__ import annotations

from typing import Dict, Callable

from .enums import GenerationMode, ReportSectionKey
from .llm_client import BaseLLMClient, MockLLMClient
from .prompt_builder import PromptBuilder
from .schemas import EvaluationContext, ReportDraft, ReportSection
from .section_catalog import SECTION_TITLES
from .templates import (
    render_conduta,
    render_demanda,
    render_fechamento,
    render_historia_pessoal,
    render_identificacao,
    render_procedimentos,
    render_referencias,
)


class ReportGenerator:
    def __init__(self, llm_client: BaseLLMClient | None = None) -> None:
        self.llm_client = llm_client or MockLLMClient()
        self.prompt_builder = PromptBuilder()

        self.template_renderers: Dict[ReportSectionKey, Callable[[EvaluationContext], str]] = {
            ReportSectionKey.IDENTIFICACAO: render_identificacao,
            ReportSectionKey.DEMANDA: render_demanda,
            ReportSectionKey.PROCEDIMENTOS: render_procedimentos,
            ReportSectionKey.HISTORIA_PESSOAL: render_historia_pessoal,
            ReportSectionKey.CONDUTA: render_conduta,
            ReportSectionKey.FECHAMENTO: render_fechamento,
            ReportSectionKey.REFERENCIAS: render_referencias,
        }

    def generate_draft(self, context: EvaluationContext) -> ReportDraft:
        draft = ReportDraft(model_name=context.model_name)
        ordered_sections = [
            ReportSectionKey.IDENTIFICACAO,
            ReportSectionKey.DEMANDA,
            ReportSectionKey.PROCEDIMENTOS,
            ReportSectionKey.HISTORIA_PESSOAL,
            ReportSectionKey.CAPACIDADE_COGNITIVA_GLOBAL,
            ReportSectionKey.FUNCOES_EXECUTIVAS,
            ReportSectionKey.LINGUAGEM,
            ReportSectionKey.GNOSIAS_PRAXIAS,
            ReportSectionKey.MEMORIA_APRENDIZAGEM,
            ReportSectionKey.ATENCAO,
            ReportSectionKey.RAVLT,
            ReportSectionKey.FDT,
            ReportSectionKey.ETDAH_PAIS,
            ReportSectionKey.ETDAH_AD,
            ReportSectionKey.SCARED,
            ReportSectionKey.EPQJ,
            ReportSectionKey.SRS2,
            ReportSectionKey.CONCLUSAO,
            ReportSectionKey.CONDUTA,
            ReportSectionKey.FECHAMENTO,
            ReportSectionKey.REFERENCIAS,
        ]

        for key in ordered_sections:
            draft.add_section(self.generate_section(key, context))

        return draft

    def generate_section(self, key: ReportSectionKey, context: EvaluationContext) -> ReportSection:
        if key in self.template_renderers:
            text = self.template_renderers[key](context)
            generated_by = GenerationMode.TEMPLATE.value
        else:
            prompt = self.prompt_builder.build_section_prompt(SECTION_TITLES[key], context)
            response = self.llm_client.generate(prompt)
            text = response.text
            generated_by = GenerationMode.LLM.value

        return ReportSection(
            key=key,
            title=SECTION_TITLES[key],
            text=text,
            generated_by=generated_by,
        )
