from __future__ import annotations

from pprint import pprint

from .compiler import ReportCompiler
from .consistency import ConsistencyChecker
from .context_builder import EvaluationContextBuilder
from .section_generators import ReportGenerator


EXAMPLE_PAYLOAD = {
    "author_name": "Jacqueline Oliveira Caires",
    "author_registry": "CRP 09/6017",
    "patient": {
        "nome": "João Vitor Campos Coelho Costa",
        "sexo": "Masculino",
        "data_nascimento": "01/01/2015",
        "idade_texto": "10 anos e 0 meses",
        "filiacao": "Nome do pai e da mãe",
        "escolaridade": "5º ano do ensino fundamental",
        "escola": "Sesc Cidadania",
    },
    "referral": {
        "interessado": "Aqui poe quem encaminhou",
        "finalidade": "Averiguação das capacidades cognitivas para auxílio diagnóstico",
        "motivo_encaminhamento": "Descrição do motivo do encaminhamento.",
    },
    "history": {
        "historia_pessoal": "Aqui entra a anamnese estruturada do paciente.",
        "observacoes_clinicas": "Paciente colaborativo, com oscilação atencional em tarefas longas.",
        "rotina_atual": "Rotina escolar e atividades extraclasse.",
        "informacoes_adicionais": "Informações complementares relevantes.",
    },
    "tests": [
        {
            "instrument": "WISC-IV",
            "computed_payload": {"QIT": 106, "ICV": 113, "IOP": 104, "IMO": 106, "IVP": 92},
            "interpretation": "Perfil intelectual globalmente preservado.",
        },
        {
            "instrument": "BPA-2",
            "computed_payload": {"AC": 51, "AD": 64, "AA": 56, "AG": 171},
            "interpretation": "Funcionamento atencional globalmente preservado.",
        },
    ],
    "report_date_city": "Goiânia",
    "report_date_text": "15 de janeiro de 2026",
}


def main() -> None:
    builder = EvaluationContextBuilder()
    context = builder.from_dict(EXAMPLE_PAYLOAD)

    generator = ReportGenerator()
    draft = generator.generate_draft(context)

    checker = ConsistencyChecker()
    consistency_report = checker.validate(context, draft)

    compiler = ReportCompiler()
    compiled = compiler.compile_markdown(draft)

    print("===== RELATÓRIO DE CONSISTÊNCIA =====")
    pprint([issue.__dict__ for issue in consistency_report.issues])

    print("\n===== LAUDO COMPILADO =====\n")
    print(compiled)


if __name__ == "__main__":
    main()
