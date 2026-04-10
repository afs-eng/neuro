from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .enums import ReportSectionKey


@dataclass
class ReferralInfo:
    interessado: str
    finalidade: str
    motivo_encaminhamento: str


@dataclass
class PatientInfo:
    nome: str
    sexo: str
    data_nascimento: str
    idade_texto: str
    filiacao: str
    escolaridade: str
    escola: str


@dataclass
class SessionInfo:
    anamnese_sessions: int = 1
    testing_sessions: int = 5
    feedback_sessions: int = 1


@dataclass
class TestResult:
    instrument: str
    applied: bool = True
    computed_payload: Dict[str, Any] = field(default_factory=dict)
    interpretation: str = ""
    raw_summary: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ClinicalHistory:
    historia_pessoal: str
    observacoes_clinicas: str = ""
    rotina_atual: str = ""
    informacoes_adicionais: str = ""


@dataclass
class StyleRules:
    use_first_name_only_in_sections: bool = True
    include_diagnostic_hypothesis: bool = True
    diagnostic_phrase: str = "hipótese diagnóstica"
    opening_phrase: str = "Em análise clínica"
    avoid_long_dashes: bool = True
    use_dsm_term: str = "DSM-5-TR™"


@dataclass
class EvaluationContext:
    author_name: str
    author_registry: str
    patient: PatientInfo
    referral: ReferralInfo
    sessions: SessionInfo
    tests: List[TestResult]
    history: ClinicalHistory
    style_rules: StyleRules = field(default_factory=StyleRules)
    references: List[str] = field(default_factory=list)
    report_date_city: str = "Goiânia"
    report_date_text: str = ""
    model_name: str = "laudo_neuropsicologico_padrao"


@dataclass
class ReportSection:
    key: ReportSectionKey
    title: str
    text: str
    source_payload: Dict[str, Any] = field(default_factory=dict)
    generated_by: str = "system"


@dataclass
class ReportDraft:
    model_name: str
    sections: List[ReportSection] = field(default_factory=list)

    def add_section(self, section: ReportSection) -> None:
        self.sections.append(section)

    def get_section(self, key: ReportSectionKey) -> Optional[ReportSection]:
        for section in self.sections:
            if section.key == key:
                return section
        return None

    def compile_text(self) -> str:
        return "\n\n".join(
            f"{section.title}\n\n{section.text}".strip()
            for section in self.sections
            if section.text.strip()
        )
