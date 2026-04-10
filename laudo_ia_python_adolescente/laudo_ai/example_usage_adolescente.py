
from laudo_ai.schemas import (
    ClinicalHistory,
    EvaluationContext,
    PatientInfo,
    ReferralInfo,
    SessionInfo,
    StyleRules,
    TestResult,
)
from laudo_ai.section_generators import ReportGenerator


def build_example_context() -> EvaluationContext:
    return EvaluationContext(
        author_name="Jacqueline Oliveira Caires",
        author_registry="CRP 09/6017",
        patient=PatientInfo(
            nome="Maria Clara Daher Costa e Silva",
            sexo="Feminino",
            data_nascimento="24/04/2011",
            idade_texto="14 anos e 8 meses",
            filiacao="João Paulo Vaz Costa e Silva e Pollyana Lucena Daher",
            escolaridade="8º ano do ensino fundamental",
            escola="",
        ),
        referral=ReferralInfo(
            interessado="Familiares",
            finalidade="Averiguação das capacidades cognitivas para auxílio diagnóstico",
            motivo_encaminhamento="Dificuldades persistentes no contexto escolar, além de prejuízos na interação social e no funcionamento emocional.",
        ),
        sessions=SessionInfo(anamnese_sessions=1, testing_sessions=5, feedback_sessions=1),
        tests=[
            TestResult("Escala Wechsler de Inteligência para Crianças – Quarta Edição (WISC-IV)"),
            TestResult("Bateria Psicológica para Avaliação da Atenção – Segunda Edição (BPA-2)"),
            TestResult("Teste dos Cinco Dígitos – FDT"),
            TestResult("Teste de Aprendizagem Auditivo-Verbal de Rey – RAVLT"),
            TestResult("Escala de Transtorno de Déficit de Atenção e Hiperatividade – Versão Pais (E-TDAH-PAIS)"),
            TestResult("Inventário de Transtorno de Déficit de Atenção e Hiperatividade – Autorrelato (E-TDAH-AD)"),
            TestResult("SCARED – Screen for Child Anxiety Related Emotional Disorders"),
            TestResult("EPQ-J – Inventário de Personalidade de Eysenck para Jovens"),
            TestResult("Escala de Responsividade Social – Segunda Edição (SRS-2)"),
        ],
        history=ClinicalHistory(
            historia_pessoal="Inserir aqui a anamnese estruturada da adolescente.",
            observacoes_clinicas="Paciente cooperativa, com lentificação cognitiva e dificuldades atencionais evidentes.",
        ),
        style_rules=StyleRules(
            use_first_name_only_in_sections=True,
            include_diagnostic_hypothesis=True,
            diagnostic_phrase="hipótese diagnóstica",
            opening_phrase="Em análise clínica",
            avoid_long_dashes=True,
            use_dsm_term="DSM-5-TR™",
        ),
        references=[
            "WECHSLER, D. WISC-IV – Escala de Inteligência Wechsler para Crianças – Quarta Edição. São Paulo: Pearson, 2013.",
            "RUEDA, F. J. M. Bateria Psicológica para Avaliação da Atenção – BPA-2. São Paulo: Vetor Editora, 2013.",
            "CONSTANTINO, J. N.; GRUBER, C. P. Social Responsiveness Scale – Second Edition (SRS-2). Torrance, CA: Western Psychological Services, 2012.",
        ],
        report_date_city="Goiânia",
        report_date_text="15 de janeiro de 2026",
        model_name="laudo_neuropsicologico_adolescente",
    )


if __name__ == "__main__":
    context = build_example_context()
    generator = ReportGenerator()
    draft = generator.generate_draft(context)
    print(draft.compile_text())
