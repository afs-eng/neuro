from __future__ import annotations

from copy import deepcopy
from io import BytesIO
import logging
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
logging.getLogger("matplotlib").setLevel(logging.WARNING)

import matplotlib.pyplot as plt
from matplotlib import font_manager
from django.conf import settings
from docx import Document
from docx.table import Table
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.shared import Inches, Pt, RGBColor
from docx.shared import Cm

from apps.reports.charts import gerar_grafico_bpa_bytes
from apps.reports.models import Report
from apps.reports.builders.references_builder import build_references
from apps.reports.services.report_context_service import ReportContextService
from apps.reports.services.ptbr_text_service import PtBrTextService
from apps.tests.srs2.interpreters import interpret_srs2_results
from apps.tests.ravlt.norms import NORMS as RAVLT_NORMS
from apps.tests.ravlt.norms import get_age_band as get_ravlt_age_band
from apps.tests.wisc4.calculators import _calcular_idade, _carregar_tabela_ncp


class ReportExportService:
    DEFAULT_TEMPLATE_PATH = settings.BASE_DIR / "PAPEL-TIMBRADO-MODELO.docx"
    ADOLESCENT_TEMPLATE_PATH = settings.BASE_DIR / "PAPEL-TIMBRADO-MODELO.docx"
    TABLE_STYLE_SOURCE_PATH = settings.BASE_DIR / "Modelo-WISC.docx"
    FONT_NAME = "Times New Roman"
    BODY_SIZE = Pt(12)
    TABLE_SIZE = Pt(9)
    TABLE_HEADER_SIZE = Pt(8)
    TITLE_SIZE = Pt(12)
    CAPTION_SIZE = Pt(9)
    BODY_FIRST_LINE_INDENT = Cm(1.5)
    BODY_LINE_SPACING = 1.5
    IDENTIFICATION_LINE_SPACING = 1.15
    HEADING_SPACE_BEFORE = Pt(10)
    HEADING_SPACE_AFTER = Pt(4)
    SUBHEADING_SPACE_BEFORE = Pt(6)
    SUBHEADING_SPACE_AFTER = Pt(2)
    BODY_SPACE_AFTER = Pt(6)
    IMAGE_WIDTH = Inches(6.2)
    DEFAULT_TABLE_WIDTH = Inches(6.5)
    HEADER_FILL = "DCE6F1"
    BPA_HEADER_FILL = "A8D08D"
    BPA_BODY_FILL = "E2EFD9"
    WISC_HEADER_FILL = "A8D08D"
    WISC_NAME_FILL = "A9D18E"
    WISC_VALUE_FILL = "E2EFD9"
    RAVLT_HEADER_FILL = "A9D08E"
    FDT_HEADER_FILL = "A8D08D"
    FDT_BODY_FILL = "E2EFD9"
    TABLE_TITLE_FILL = "538135"
    LOCAL_LIBERATION_SERIF = Path.home() / ".local/share/fonts/liberation/LiberationSerif-Regular.ttf"
    INTERPRETATION_LABELS = (
        "Interpretação clínica:",
        "Interpretação e Observações Clínicas:",
    )
    EMPTY_INTERPRETATION_MESSAGES = {
        "Nenhum instrumento específico deste domínio apresentou interpretação clínica consolidada.",
    }
    INSTRUMENT_CATALOG = {
        "anamnese": {
            "nome": "Anamnese",
            "descricao": "Entrevista clínica inicial destinada ao levantamento da história do desenvolvimento, queixas atuais, antecedentes médicos, escolares, familiares, emocionais e comportamentais, com o objetivo de contextualizar os dados obtidos nos demais instrumentos.",
        },
        "wisc4": {
            "nome": "Escala Wechsler de Inteligência para Crianças – Quarta Edição (WISC-IV)",
            "descricao": "Utilizada para avaliar o funcionamento intelectual global, os índices fatoriais (Compreensão Verbal, Organização Perceptual, Memória Operacional e Velocidade de Processamento) e fornecer indicadores sobre o perfil cognitivo.",
        },
        "wais3": {
            "nome": "Escala Wechsler de Inteligência para Adultos – Terceira Edição (WAIS-III)",
            "descricao": "Instrumento destinado à avaliação da capacidade intelectual global em adultos, permitindo analisar habilidades verbais, não verbais, memória operacional e velocidade de processamento, além de oferecer indicadores sobre o perfil cognitivo geral.",
        },
        "wasi": {
            "nome": "Escala Wechsler Abreviada de Inteligência (WASI)",
            "descricao": "Utilizada para estimar o funcionamento intelectual global, verbal e de execução, bem como fornecer indicadores breves sobre a capacidade cognitiva geral.",
        },
        "bpa2": {
            "nome": "Bateria Psicológica para Avaliação da Atenção – Segunda Edição (BPA-2)",
            "descricao": "Avalia a capacidade geral de atenção, incluindo atenção concentrada, alternada, dividida e atenção global.",
        },
        "fdt": {
            "nome": "Teste dos Cinco Dígitos (FDT)",
            "descricao": "Investiga a velocidade de processamento, controle inibitório, alternância e flexibilidade cognitiva.",
        },
        "ravlt": {
            "nome": "Teste de Aprendizagem Auditivo-Verbal de Rey (RAVLT)",
            "descricao": "Avalia memória verbal episódica, aquisição, retenção, recuperação e resistência à interferência.",
        },
        "figuras_complexas_rey": {
            "nome": "Figuras Complexas de Rey",
            "descricao": "Instrumento utilizado para avaliar habilidades visuoconstrutivas, planejamento perceptomotor e memória visual, por meio das etapas de cópia e evocação.",
        },
        "etdah_ad": {
            "nome": "Escala para Transtorno de Déficit de Atenção e Hiperatividade – Autorrelato (E-TDAH-AD)",
            "descricao": "Questionário destinado à identificação de sintomas relacionados à desatenção, impulsividade, hiperatividade, aspectos emocionais e dificuldades funcionais associadas ao TDAH, com base no autorrelato.",
        },
        "etdah_pais": {
            "nome": "Escala para Transtorno de Déficit de Atenção e Hiperatividade – Versão Pais (E-TDAH-PAIS)",
            "descricao": "Questionário para identificação de sintomas de desatenção, impulsividade, hiperatividade, regulação emocional e comportamento adaptativo, a partir da percepção dos responsáveis.",
        },
        "scared": {
            "nome": "SCARED – Autorrelato (Screen for Child Anxiety Related Emotional Disorders)",
            "descricao": "Avalia sintomas ansiosos em crianças e adolescentes, incluindo ansiedade generalizada, ansiedade de separação, fobia social, pânico e sintomas somáticos, com base no autorrelato.",
        },
        "scared_mae": {
            "nome": "SCARED – Versão Mãe",
            "descricao": "Avalia sintomas ansiosos, incluindo ansiedade generalizada, de separação, fobia social e somatizações, a partir da percepção materna.",
        },
        "srs2": {
            "nome": "Escala de Responsividade Social – Segunda Edição (SRS-2)",
            "descricao": "Rastreia dificuldades em comunicação social, cognição social, padrões restritos e repetitivos e comportamentos associados ao espectro autista.",
        },
        "epq_j": {
            "nome": "Inventário de Personalidade de Eysenck para Jovens (EPQ-J)",
            "descricao": "Avalia traços de personalidade em crianças e adolescentes, contemplando dimensões como extroversão, neuroticismo, psicoticismo e sinceridade.",
        },
        "bfp": {
            "nome": "Bateria Fatorial de Personalidade (BFP)",
            "descricao": "Instrumento fundamentado no modelo dos Cinco Grandes Fatores, destinado à avaliação dos traços de personalidade: neuroticismo, extroversão, socialização, realização e abertura à experiência.",
        },
        "iphexa": {
            "nome": "Inventário de Personalidade HEXA-Flexível para Adultos (IPHEXA)",
            "descricao": "Avalia traços de personalidade com base em dimensões amplas do funcionamento da personalidade, contribuindo para a compreensão do estilo emocional, interpessoal e adaptativo do avaliado.",
        },
        "bai": {
            "nome": "Inventário de Ansiedade de Beck (BAI)",
            "descricao": "Instrumento de autorrelato utilizado para mensurar a intensidade de sintomas ansiosos, com ênfase em manifestações fisiológicas e subjetivas de ansiedade.",
        },
        "bdi": {
            "nome": "Inventário de Depressão de Beck (BDI)",
            "descricao": "Instrumento de autorrelato utilizado para avaliar a intensidade de sintomas depressivos, incluindo aspectos afetivos, cognitivos, motivacionais e somáticos.",
        },
        "ebadep_a": {
            "nome": "Escala Baptista de Depressão – Versão Adulto (EBADEP-A)",
            "descricao": "Avalia a presença e a intensidade de sintomas depressivos em adultos, contemplando aspectos emocionais, cognitivos, comportamentais e fisiológicos.",
        },
        "ebadep_ij": {
            "nome": "Escala Baptista de Depressão – Versão Infantojuvenil (EBADEP-IJ)",
            "descricao": "Instrumento destinado à identificação de sintomas depressivos em crianças e adolescentes, abrangendo indicadores emocionais, cognitivos e comportamentais.",
        },
        "ebaped_ij": {
            "nome": "Escala Baptista de Depressão – Versão Infantojuvenil (EBADEP-IJ)",
            "descricao": "Instrumento destinado à identificação de sintomas depressivos em crianças e adolescentes, abrangendo indicadores emocionais, cognitivos e comportamentais.",
        },
        "scq": {
            "nome": "Social Communication Questionnaire (SCQ)",
            "descricao": "Questionário de rastreio voltado à identificação de dificuldades na comunicação social e comportamentos associados ao Transtorno do Espectro Autista.",
        },
        "cars2_hf": {
            "nome": "Childhood Autism Rating Scale – High Functioning (CARS2-HF)",
            "descricao": "Escala destinada à avaliação de comportamentos associados ao Transtorno do Espectro Autista em indivíduos com maior nível de funcionamento, considerando interação social, comunicação, flexibilidade e padrões comportamentais.",
        },
        "mchat": {
            "nome": "Modified Checklist for Autism in Toddlers (M-CHAT)",
            "descricao": "Instrumento de rastreio precoce para sinais de risco para Transtorno do Espectro Autista em crianças pequenas, com foco em interação social, atenção compartilhada e comportamentos comunicativos.",
        },
        "son_r_2_5_7": {
            "nome": "SON-R 2½–7[a]",
            "descricao": "Teste não verbal de inteligência utilizado para avaliar o raciocínio geral, a percepção visual e a organização espacial, minimizando a influência da linguagem.",
        },
        "thcp": {
            "nome": "Teste de Habilidades Cognitivas Primárias (THCP)",
            "descricao": "Instrumento utilizado para investigar habilidades cognitivas básicas relacionadas ao desenvolvimento infantil, contribuindo para a análise do perfil cognitivo e do potencial de aprendizagem.",
        },
        "mmse_2": {
            "nome": "Miniexame do Estado Mental – Segunda Edição (MMSE-2)",
            "descricao": "Instrumento de rastreio cognitivo utilizado para avaliar orientação, atenção, memória, linguagem e habilidades construtivas, auxiliando na investigação de possíveis alterações cognitivas.",
        },
        "vineland": {
            "nome": "Vineland – Escala de Comportamento Adaptativo",
            "descricao": "Avalia o comportamento adaptativo em domínios como comunicação, socialização, habilidades de vida diária e, em algumas versões, habilidades motoras, contribuindo para a compreensão do funcionamento adaptativo global.",
        },
        "portage": {
            "nome": "Portage",
            "descricao": "Instrumento utilizado para avaliação do desenvolvimento infantil em diferentes áreas, como linguagem, cognição, socialização, autocuidados e desenvolvimento motor.",
        },
        "htp": {
            "nome": "HTP (House-Tree-Person)",
            "descricao": "Técnica projetiva gráfica utilizada para investigação de aspectos emocionais, vivenciais e da dinâmica da personalidade, por meio da interpretação dos desenhos da casa, árvore e pessoa.",
        },
    }
    PROCEDURES_ORDER = [
        "anamnese",
        "wisc4",
        "wais3",
        "wasi",
        "son_r_2_5_7",
        "thcp",
        "mmse_2",
        "vineland",
        "portage",
        "bpa2",
        "fdt",
        "ravlt",
        "figuras_complexas_rey",
        "etdah_pais",
        "etdah_ad",
        "scared",
        "scared_mae",
        "srs2",
        "epq_j",
        "bfp",
        "iphexa",
        "bai",
        "bdi",
        "ebadep_a",
        "ebadep_ij",
        "ebaped_ij",
        "scq",
        "cars2_hf",
        "mchat",
        "htp",
    ]

    @staticmethod
    def generate_html(report: Report):
        ReportContextService.sync_report_context(report)
        content = str(report.final_text or report.edited_text or "")
        created_at = report.created_at.strftime("%d/%m/%Y") if report.created_at else ""
        patient_name = report.patient.full_name if report.patient else ""
        author_name = report.author.display_name if report.author else "Sistema"
        interested_party = report.interested_party or patient_name
        purpose = report.purpose or "Auxílio diagnóstico e planejamento clínico."

        return f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Times New Roman', serif; line-height: 1.5; color: #222; font-size: 12pt; }}
                h1 {{ text-align: center; font-size: 16pt; }}
                .metadata {{ margin-bottom: 24px; }}
            </style>
        </head>
        <body>
            <h1>{report.title}</h1>
            <div class="metadata">
                <p><b>Paciente:</b> {patient_name}</p>
                <p><b>Profissional:</b> {author_name}</p>
                <p><b>Interessado:</b> {interested_party}</p>
                <p><b>Finalidade:</b> {purpose}</p>
                <p><b>Data:</b> {created_at}</p>
            </div>
            <div>{content.replace(chr(10), "<br>")}</div>
        </body>
        </html>
        """

    @classmethod
    def generate_docx_bytes(cls, report: Report) -> bytes:
        context = ReportContextService.sync_report_context(report)
        context = dict(context) if isinstance(context, dict) else {}
        sections = {
            section.key: str(section.content_edited or section.content_generated or "")
            for section in report.sections.all()
        }

        template_path = cls._select_template_path(report)
        if not template_path.exists():
            raise FileNotFoundError(
                f"Template DOCX não encontrado: {template_path.name}"
            )

        if cls._is_adolescent_context(context, report):
            document = cls._build_adolescent_document(report, context, sections)
        else:
            document = Document(str(template_path))
            cls._ensure_model_table_styles(document)
            cls._apply_base_styles(document)
            cls._replace_simple_sections(document, sections)
            cls._rebuild_qualitative_section(document, sections, context)

        cls._ensure_model_table_styles(document)
        cls._normalize_model_header_footer(document)

        output = BytesIO()
        document.save(output)
        return output.getvalue()

    @classmethod
    def _select_template_path(cls, report: Report):
        patient = getattr(report, "patient", None)
        age = getattr(patient, "age", None)
        if age is not None and age < 18 and cls.ADOLESCENT_TEMPLATE_PATH.exists():
            return cls.ADOLESCENT_TEMPLATE_PATH
        return cls.DEFAULT_TEMPLATE_PATH

    @classmethod
    def _is_adolescent_document(cls, document: Document, context: dict) -> bool:
        if any(
            paragraph.text.strip() == "Interessado Familiares"
            for paragraph in document.paragraphs
        ):
            return True
        birth_date = (context.get("patient") or {}).get("birth_date") or ""
        if birth_date:
            try:
                from datetime import date

                year, month, day = map(int, birth_date.split("-"))
                born = date(year, month, day)
                today = date.today()
                age = (
                    today.year
                    - born.year
                    - ((today.month, today.day) < (born.month, born.day))
                )
                return age < 18
            except ValueError:
                return False
        return False

    @classmethod
    def _is_adolescent_context(cls, context: dict, report) -> bool:
        patient = getattr(report, "patient", None)
        age = getattr(patient, "age", None)
        if age is not None:
            return age < 18
        birth_date = (context.get("patient") or {}).get("birth_date") or ""
        if birth_date:
            try:
                from datetime import date

                year, month, day = map(int, birth_date.split("-"))
                born = date(year, month, day)
                today = date.today()
                return (
                    today.year
                    - born.year
                    - ((today.month, today.day) < (born.month, born.day))
                ) < 18
            except ValueError:
                return False
        return False

    @classmethod
    def _build_adolescent_document(
        cls, report, context: dict, sections: dict[str, str]
    ):
        template_path = cls._select_template_path(report)
        document = (
            Document(str(template_path)) if template_path.exists() else Document()
        )
        cls._ensure_model_table_styles(document)
        cls._clear_document_body(document)
        cls._apply_base_styles(document)
        patient = context.get("patient") or {}
        evaluation = context.get("evaluation") or {}
        author_name = getattr(
            getattr(report, "author", None), "display_name", "Profissional responsável"
        )
        interested_party = (
            report.interested_party
            or patient.get("responsible_name")
            or patient.get("full_name")
            or "Familiares"
        )
        table_index = 1
        chart_index = 1
        def append_table_with_interpretation(
            rows,
            table_key: str,
            interpretation: str | None,
            caption: str,
        ):
            nonlocal table_index
            cls._append_table_with_interpretation(
                document,
                rows,
                table_key,
                interpretation,
                caption=cls._table_caption_text(table_index, caption),
            )
            if rows:
                table_index += 1

        def append_chart(
            caption: str,
            image_bytes: bytes | None,
            note: str | None = None,
            width=None,
            show_caption: bool = True,
        ):
            nonlocal chart_index
            if not image_bytes:
                return
            cls._append_chart(
                document,
                cls._chart_caption_text(chart_index, caption) if show_caption else None,
                image_bytes,
                width=width,
            )
            if note:
                note_paragraph = document.add_paragraph(note)
                cls._format_chart_legend_paragraph(note_paragraph)
            chart_index += 1

        def section_or_test_interpretation(
            section_key: str,
            fallback_section_key: str | None,
            test_payload: dict | None,
        ) -> str:
            return cls._resolve_interpretation_text(
                sections.get(section_key),
                sections.get(fallback_section_key) if fallback_section_key else None,
                test_payload,
            )

        purpose = (
            report.purpose
            or evaluation.get("evaluation_purpose")
            or evaluation.get("referral_reason")
            or "Averiguação das capacidades cognitivas para auxílio diagnóstico"
        )

        cls._add_center_title(document, "LAUDO DE AVALIAÇÃO NEUROPSICOLÓGICA")
        cls._add_center_text(
            document,
            "De acordo com a Resolução de Elaboração de Documentos-CFP 006/2019",
        )

        cls._append_heading(document, "1. IDENTIFICAÇÃO")
        cls._append_subheading(document, "1.1. Identificação do Laudo")
        cls._append_label_value(document, "Autora", author_name)
        cls._append_label_value(document, "Interessado", interested_party)
        cls._append_label_value(document, "Finalidade", purpose)
        cls._append_subheading(document, "1.2. Identificação do Paciente")
        cls._append_label_value(
            document, "Nome", patient.get("full_name") or "Não informado"
        )
        cls._append_label_value(
            document, "Sexo", cls._format_sex_display(patient.get("sex"))
        )
        cls._append_label_value(
            document,
            "Data de nascimento",
            cls._format_date_display(patient.get("birth_date")),
        )
        cls._append_label_value(document, "Idade", cls._age_text(context))
        cls._append_label_value(document, "Filiação", cls._filiation_text(patient))
        cls._append_label_value(document, "Escolaridade", cls._schooling_text(patient))
        if patient.get("school_name"):
            cls._append_label_value(document, "Escola", patient.get("school_name"))

        cls._append_heading(document, "2. DESCRIÇÃO DA DEMANDA")
        cls._append_subheading(document, "2.1. Motivo do Encaminhamento")
        cls._append_paragraph(
            document,
            sections.get("descricao_demanda")
            or evaluation.get("referral_reason")
            or "Sem conteúdo disponível para esta seção.",
        )

        cls._append_heading(document, "3. PROCEDIMENTOS")
        cls._append_paragraph(document, cls._procedures_intro(context))
        for item in cls._adolescent_instruments(context):
            cls._append_bullet(document, f"{item['name']}: {item['description']}")

        cls._append_heading(document, "4. ANÁLISE")
        cls._append_subheading(document, "4.1. História Pessoal")
        cls._append_paragraph(
            document,
            sections.get("historia_pessoal")
            or "Sem conteúdo disponível para esta seção.",
        )

        patient_title = "da paciente" if (context.get("patient") or {}).get("sex") == "F" else "do paciente"
        cls._append_heading(document, "5. ANÁLISE QUALITATIVA")
        cls._append_subheading(document, f"5.1. Desempenho {patient_title} no WISC-IV")
        wisc_test = cls._find_test(context, "wisc4")
        wisc_chart = cls._wisc_chart(wisc_test)
        append_chart(
            "WISC-IV - INDICES DE QIS",
            wisc_chart,
            cls._wisc_chart_legend(chart_index),
            show_caption=False,
        )
        cls._append_wisc_global_block(document, wisc_test, context)
        cls._append_subheading(document, "5.2. Subescalas WISC-IV")
        cls._append_subheading(document, "5.2.1. Função Executiva")
        append_table_with_interpretation(
            cls._wisc_rows(
                cls._find_test(context, "wisc4"), context, "funcoes_executivas"
            ),
            "wisc",
            sections.get("funcoes_executivas"),
            "Resultado da Função executiva",
        )
        cls._append_subheading(document, "5.2.2. Linguagem")
        append_table_with_interpretation(
            cls._wisc_rows(cls._find_test(context, "wisc4"), context, "linguagem"),
            "wisc",
            sections.get("linguagem"),
            "Resultado da Linguagem",
        )
        cls._append_subheading(document, "5.2.3. Gnosias e Praxias")
        append_table_with_interpretation(
            cls._wisc_rows(
                cls._find_test(context, "wisc4"), context, "gnosias_praxias"
            ),
            "wisc",
            sections.get("gnosias_praxias"),
            "Resultados da Gnosias e praxias",
        )
        cls._append_subheading(document, "5.2.4. Memória e Aprendizagem")
        append_table_with_interpretation(
            cls._wisc_memory_rows(cls._find_test(context, "wisc4"), context),
            "wisc",
            sections.get("memoria_aprendizagem"),
            "Resultados da Memória e aprendizagem",
        )

        cls._append_heading(
            document,
            "6. BPA-2 – BATERIA PSICOLÓGICA PARA AVALIAÇÃO DA ATENÇÃO",
        )
        cls._append_paragraph(
            document,
            "A Bateria Psicológica para Avaliação da Atenção-2 (BPA-2) mensura a capacidade geral de atenção, avaliando individualmente atenção concentrada, dividida, alternada e geral.",
        )
        append_table_with_interpretation(
            cls._bpa_rows(cls._find_test(context, "bpa2"), context),
            "bpa",
            sections.get("bpa2") or sections.get("atencao"),
            "Atenção BPA-2 Resultados",
        )
        append_chart(
            "BPA-2 apresenta os resultados da avaliação da atenção",
            cls._bpa_chart_bytes(cls._find_test(context, "bpa2")),
        )

        cls._append_heading(
            document,
            "7. RAVLT – REY AUDITORY VERBAL LEARNING TEST",
        )
        cls._append_paragraph(
            document,
            "O RAVLT avalia memória verbal, capacidade de aprendizado auditivo e retenção de informações ao longo do tempo.",
        )
        ravlt_interpretation = sections.get("ravlt") or sections.get("memoria_aprendizagem")
        append_table_with_interpretation(
            cls._ravlt_rows(cls._find_test(context, "ravlt"), context),
            "ravlt",
            None,
            cls._ravlt_table_caption(),
        )
        cls._append_ravlt_conceptual_paragraph(document)
        if ravlt_interpretation:
            cls._append_interpretation_block(
                document, cls._normalize_interpretation_text(ravlt_interpretation)
            )
        append_chart("RAVLT Resultados", cls._ravlt_chart(cls._find_test(context, "ravlt")))

        cls._append_heading(
            document, "8. FDT – TESTE DOS CINCO DÍGITOS"
        )
        cls._append_paragraph(
            document,
            "O FDT avalia processos automáticos e controlados, incluindo velocidade de processamento, controle inibitório, alternância e flexibilidade cognitiva.",
        )
        append_table_with_interpretation(
            cls._fdt_rows(cls._find_test(context, "fdt")),
            "fdt",
            sections.get("fdt") or sections.get("funcoes_executivas"),
            "TABELA FDT- PROCESSOS AUTOMÁTICOS E CONTROLADOS",
        )
        append_chart(
            "FDT - Processos Automático",
            cls._fdt_chart(cls._find_test(context, "fdt"), automatic=True),
        )
        append_chart(
            "FDT - Processos Controlados",
            cls._fdt_chart(cls._find_test(context, "fdt"), automatic=False),
        )

        if cls._find_test(context, "etdah_pais"):
            cls._append_heading(document, "9. E-TDAH-PAIS")
            cls._append_paragraph(
                document,
                "A Escala E-TDAH-PAIS identifica manifestações comportamentais e emocionais associadas ao TDAH a partir da percepção dos responsáveis.",
            )
            append_table_with_interpretation(
                cls._etdah_rows(cls._find_test(context, "etdah_pais")),
                "etdah",
                section_or_test_interpretation(
                    "etdah_pais", None, cls._find_test(context, "etdah_pais")
                ),
                "Resultados do E-TDAH-PAIS",
            )
            append_chart(
                "E-TDAH-PAIS Resultados",
                cls._etdah_chart(cls._find_test(context, "etdah_pais")),
            )

        if cls._find_test(context, "etdah_ad"):
            cls._append_heading(document, "10. E-TDAH-AD")
            cls._append_paragraph(
                document,
                "O E-TDAH-AD investiga sintomas relacionados à atenção, hiperatividade, impulsividade e aspectos emocionais a partir do autorrelato do adolescente.",
            )
            append_table_with_interpretation(
                cls._etdah_rows(cls._find_test(context, "etdah_ad")),
                "etdah",
                section_or_test_interpretation(
                    "etdah_ad", None, cls._find_test(context, "etdah_ad")
                ),
                "Resultados do E-TDAH-AD",
            )
            append_chart(
                "E-TDAH-AD Resultados",
                cls._etdah_chart(cls._find_test(context, "etdah_ad")),
            )

        scared_tests = cls._find_tests(context, "scared")
        if scared_tests:
            cls._append_heading(
                document,
                "11. SCARED",
            )
            cls._append_paragraph(
                document,
                "O SCARED rastreia sintomas ansiosos, incluindo pânico, ansiedade generalizada, ansiedade de separação, fobia social e evitação escolar.",
            )
            for scared_test in scared_tests:
                form_label = cls._scared_form_label(scared_test)
                append_table_with_interpretation(
                    cls._scared_rows(scared_test),
                    "scared",
                    section_or_test_interpretation(
                        "scared",
                        None,
                        scared_test,
                    ),
                    f"SCARED - Resultados {form_label}",
                )
                append_chart(
                    f"SCARED Resultados {form_label}",
                    cls._scared_chart(scared_test),
                )

        if cls._find_test(context, "epq_j"):
            cls._append_heading(
                document,
                "12. EPQ-J",
            )
            append_table_with_interpretation(
                cls._epq_rows(cls._find_test(context, "epq_j")),
                "epq",
                section_or_test_interpretation(
                    "epq_j", None, cls._find_test(context, "epq_j")
                ),
                "EPQ-J Resultados da personalidade",
            )
            append_chart(
                "EPQ-J Resultados dos percentis",
                cls._epq_chart(cls._find_test(context, "epq_j")),
            )

        if cls._find_test(context, "srs2"):
            srs2_test = cls._find_test(context, "srs2")
            cls._append_heading(
                document,
                "13. SRS-2 – ESCALA DE RESPONSIVIDADE SOCIAL",
            )
            cls._append_paragraph(
                document,
                "A SRS-2 avalia aspectos da interação social e comportamentos associados ao espectro autista, exigindo sempre integração clínica cuidadosa.",
            )
            append_table_with_interpretation(
                cls._srs2_rows(srs2_test),
                "srs2",
                section_or_test_interpretation(
                    "srs2", None, srs2_test
                ),
                "SRS-2 Resultados",
            )
            append_chart(
                "SRS-2 Resultados",
                cls._srs2_chart(srs2_test),
            )
        cls._append_heading(document, "14. CONCLUSÃO")
        cls._append_paragraph(
            document,
            sections.get("conclusao") or "Sem conteúdo disponível para esta seção.",
        )
        cls._append_heading(document, "15. SUGESTÕES DE CONDUTA (ENCAMINHAMENTOS)")
        for bullet in cls._split_bullets(sections.get("sugestoes_conduta") or ""):
            cls._append_bullet(document, bullet)

        cls._append_heading(document, "16. A EQUIPE MULTIDISCIPLINAR")
        for paragraph in cls._team_paragraphs(report):
            cls._append_paragraph(document, paragraph)
        for line in cls._signature_lines(report):
            cls._append_paragraph(
                document,
                line,
                center=line.startswith(
                    (
                        author_name.split(" ")[0],
                        getattr(getattr(report, "author", None), "display_name", "")[
                            :1
                        ],
                    )
                )
                if line
                else False,
            )

        cls._append_heading(document, "17. IMPORTANTE RESSALTAR QUE ESTE DOCUMENTO:")
        for item in cls._important_document_items():
            cls._append_numbered_item(document, item)

        cls._append_heading(document, "18. REFERÊNCIA BIBLIOGRÁFICA")
        for ref in cls._references_list(context):
            cls._append_paragraph(document, ref)
        return document

    @classmethod
    def _apply_base_styles(cls, document: Document):
        cls._apply_page_layout(document)
        for style_name in ("Normal",):
            style = document.styles[style_name]
            style.font.name = cls.FONT_NAME
            style.font.size = cls.BODY_SIZE
            style.paragraph_format.space_before = Pt(0)
            style.paragraph_format.space_after = cls.BODY_SPACE_AFTER
            style.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
            style.paragraph_format.first_line_indent = cls.BODY_FIRST_LINE_INDENT
            style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    @classmethod
    def _apply_page_layout(cls, document: Document):
        for section in document.sections:
            section.top_margin = Cm(3)
            section.bottom_margin = Cm(2)
            section.left_margin = Cm(2)
            section.right_margin = Cm(2)
            section.header_distance = Cm(1.27)
            section.footer_distance = Cm(1.27)
            sect_pr = section._sectPr
            pg_mar = sect_pr.find(qn("w:pgMar"))
            if pg_mar is None:
                pg_mar = OxmlElement("w:pgMar")
                sect_pr.append(pg_mar)
            pg_mar.set(qn("w:gutter"), "0")

    @classmethod
    def _normalize_model_header_footer(cls, document: Document):
        for section in document.sections:
            for paragraph in section.footer.paragraphs:
                for run in paragraph.runs:
                    if run.text == "pág. ":
                        run.text = "pág."

    @classmethod
    def _ensure_model_table_styles(cls, document: Document):
        try:
            document.styles["Table Grid"]
            return
        except KeyError:
            pass

        source_path = cls.TABLE_STYLE_SOURCE_PATH
        if not source_path.exists():
            return

        source_document = Document(str(source_path))
        source_styles = source_document.styles.element
        target_styles = document.styles.element

        existing_ids = {
            style.get(qn("w:styleId"))
            for style in target_styles.findall(qn("w:style"))
        }

        for style_id in ("Tabelanormal", "Tabelacomgrade", "Tabelacomgrade1"):
            if style_id in existing_ids:
                continue
            source_style = source_styles.find(f'.//w:style[@w:styleId="{style_id}"]', namespaces={"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"})
            if source_style is not None:
                target_styles.append(deepcopy(source_style))

    @classmethod
    def _apply_model_table_style(cls, table):
        for style_name in ("Table Grid", "Tabela com grade1"):
            try:
                table.style = style_name
                return
            except KeyError:
                continue

    @classmethod
    def _replace_simple_sections(cls, document: Document, sections: dict[str, str]):
        replacements = {
            "IDENTIFICAÇÃO": sections.get(
                "identificacao", "Sem conteúdo disponível para esta seção."
            ),
            "DESCRIÇÃO DA DEMANDA": sections.get(
                "descricao_demanda", "Sem conteúdo disponível para esta seção."
            ),
            "PROCEDIMENTOS": sections.get(
                "procedimentos", "Sem conteúdo disponível para esta seção."
            ),
            "ANÁLISE": sections.get(
                "historia_pessoal", "Sem conteúdo disponível para esta seção."
            ),
            "Conclusão": sections.get(
                "conclusao", "Sem conteúdo disponível para esta seção."
            ),
            "Sugestões de Conduta (Encaminhamentos):": sections.get(
                "sugestoes_conduta", "Sem conteúdo disponível para esta seção."
            ),
            "Referências Bibliográficas": sections.get(
                "referencias_bibliograficas",
                "Sem conteúdo disponível para esta seção.",
            ),
            "Referencia Bibliográfica": sections.get(
                "referencias_bibliograficas",
                "Sem conteúdo disponível para esta seção.",
            ),
        }
        boundaries = {
            "IDENTIFICAÇÃO": "DESCRIÇÃO DA DEMANDA",
            "DESCRIÇÃO DA DEMANDA": "PROCEDIMENTOS",
            "PROCEDIMENTOS": "ANÁLISE",
            "ANÁLISE": "ANÁLISE QUALIDATIVA",
            "Conclusão": "Sugestões de Conduta (Encaminhamentos):",
            "Sugestões de Conduta (Encaminhamentos):": "Considerações Finais",
            "Referências Bibliográficas": None,
            "Referencia Bibliográfica": None,
        }

        for heading, text in replacements.items():
            cls._replace_block_between_headings(
                document, heading, boundaries.get(heading), text
            )

    @classmethod
    def _replace_block_between_headings(
        cls, document: Document, start_heading: str, end_heading: str | None, text: str
    ):
        start = cls._find_paragraph(document, start_heading)
        if start is None:
            return
        end = cls._find_paragraph(document, end_heading) if end_heading else None
        cls._remove_nodes_between(start, end)
        anchor = start
        for line in (text or "Sem conteúdo disponível para esta seção.").split("\n"):
            anchor = cls._insert_paragraph_after(anchor, "")
            cls._append_body_text_with_bold_label(anchor, line)
            cls._format_body_paragraph(anchor)

    @classmethod
    def _rebuild_qualitative_section(
        cls, document: Document, sections: dict[str, str], context: dict
    ):
        start = cls._find_paragraph(document, "ANÁLISE QUALIDATIVA")
        end = cls._find_paragraph(document, "Conclusão")
        if start is None or end is None:
            return

        cls._remove_nodes_between(start, end)
        tests = {
            item.get("instrument_code"): item
            for item in context.get("validated_tests") or []
        }
        is_adolescent = cls._is_adolescent_document(document, context)
        table_index = 1
        chart_index = 1
        anchor = start
        def add_title(text: str):
            nonlocal anchor
            anchor = cls._insert_paragraph_after(anchor, PtBrTextService.normalize(text))
            cls._format_subtitle_paragraph(anchor)

        def add_text(text: str):
            nonlocal anchor
            text = PtBrTextService.normalize(text)
            for line in (text or "").split("\n"):
                if not line.strip():
                    continue
                if line.lstrip().startswith("- "):
                    anchor = cls._insert_paragraph_after(anchor, "")
                    bullet_text = line.lstrip()[2:].strip()
                    p = anchor
                    lead, separator, tail = bullet_text.partition(" Avaliou ")
                    bullet_prefix = p.add_run("-\t")
                    bullet_prefix.font.name = cls.FONT_NAME
                    bullet_prefix.font.size = cls.BODY_SIZE
                    bold_run = p.add_run(lead if separator else bullet_text)
                    bold_run.font.name = cls.FONT_NAME
                    bold_run.font.size = cls.BODY_SIZE
                    bold_run.bold = True
                    if separator:
                        tail_run = p.add_run(f" Avaliou {tail}")
                        tail_run.font.name = cls.FONT_NAME
                        tail_run.font.size = cls.BODY_SIZE
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    p.paragraph_format.space_before = Pt(0)
                    p.paragraph_format.space_after = cls.BODY_SPACE_AFTER
                    p.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
                    p.paragraph_format.left_indent = Cm(1.1)
                    p.paragraph_format.first_line_indent = Cm(-0.55)
                    p.paragraph_format.tab_stops.add_tab_stop(Cm(1.1))
                else:
                    anchor = cls._insert_paragraph_after(anchor, "")
                    cls._append_body_text_with_bold_label(anchor, line)
                    if line.startswith("Capacidade Cognitiva Global:"):
                        cls._append_wisc_intro_paragraph(anchor, line)
                    else:
                        cls._format_left_body_paragraph(anchor)

        def add_table(caption: str, rows: list[list[str]] | None, table_key: str):
            nonlocal anchor, table_index
            if not rows:
                return
            if table_key == "ravlt":
                table = cls._insert_ravlt_table_after(anchor, rows)
            else:
                table = cls._insert_table_after(anchor, rows, table_key)
                cls._format_table(table, table_key)
            anchor = cls._insert_paragraph_after_table(
                table, cls._table_caption_text(table_index, caption)
            )
            cls._format_caption_paragraph(anchor)
            table_index += 1

        def add_chart(
            caption: str,
            image_bytes: bytes | None,
            note: str | None = None,
            width=None,
            show_caption: bool = True,
        ):
            nonlocal anchor, chart_index
            if not image_bytes:
                return
            anchor = cls._insert_paragraph_after(anchor, "")
            run = anchor.runs[0] if anchor.runs else anchor.add_run()
            run.add_picture(BytesIO(image_bytes), width=width or cls.IMAGE_WIDTH)
            anchor.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if show_caption:
                anchor = cls._insert_paragraph_after(
                    anchor, cls._chart_caption_text(chart_index, caption)
                )
                cls._format_caption_paragraph(anchor)
            if note:
                anchor = cls._insert_paragraph_after(anchor, note)
                cls._format_chart_legend_paragraph(anchor)
            chart_index += 1

        patient_title = "da paciente" if (context.get("patient") or {}).get("sex") == "F" else "do paciente"
        add_title(f"5.1. Desempenho {patient_title} no WISC-IV")
        add_chart(
            "WISC-IV - INDICES DE QIS",
            cls._wisc_chart(tests.get("wisc4")),
            cls._wisc_chart_legend(chart_index),
            show_caption=False,
        )
        add_text(cls._wisc_global_intro_text(tests.get("wisc4"), context))
        for lead, tail in cls._wisc_global_bullet_parts(tests.get("wisc4")):
            add_text(f"- {lead} {tail}")

        if is_adolescent:
            add_title("5.2. Subescalas WISC-IV")
            add_title("5.2.1. Função Executiva")
            add_text(sections.get("funcoes_executivas", ""))
            add_table(
                "Resultado da Função executiva",
                cls._wisc_rows(tests.get("wisc4"), context, "funcoes_executivas"),
                "wisc",
            )

            add_title("5.2.2. Linguagem")
            add_text(sections.get("linguagem", ""))
            add_table(
                "Resultados da Linguagem",
                cls._wisc_rows(tests.get("wisc4"), context, "linguagem"),
                "wisc",
            )

            add_title("5.2.3. Gnosias e Praxias")
            add_text(sections.get("gnosias_praxias", ""))
            add_table(
                "Resultados da Gnosias e praxias",
                cls._wisc_rows(tests.get("wisc4"), context, "gnosias_praxias"),
                "wisc",
            )

            add_title("5.2.4. Memória e Aprendizagem")
            add_text(sections.get("memoria_aprendizagem", ""))
            add_table(
                "Resultados da Memória e aprendizagem",
                cls._wisc_memory_rows(tests.get("wisc4"), context),
                "wisc",
            )

            add_title("6. BPA-2 Bateria Psicológica para Avaliação da Atenção")
            add_text(sections.get("atencao", ""))
            add_table("Atenção BPA-2 Resultados", cls._bpa_rows(tests.get("bpa2"), context), "bpa")
            add_chart(
                "BPA-2 apresenta os resultados da avaliação da atenção",
                cls._bpa_chart_bytes(tests.get("bpa2")),
            )

            add_title("7. RAVLT Rey Auditory Verbal Learning Test")
            ravlt_interpretation = sections.get("ravlt", sections.get("memoria_aprendizagem", ""))
            add_table(
                cls._ravlt_table_caption(), cls._ravlt_rows(tests.get("ravlt"), context), "ravlt"
            )
            anchor = cls._insert_ravlt_conceptual_paragraph_after(anchor)
            if ravlt_interpretation:
                anchor = cls._insert_interpretation_block_after(
                    anchor, cls._normalize_interpretation_text(ravlt_interpretation)
                )
            add_chart("RAVLT Resultados", cls._ravlt_chart(tests.get("ravlt")))

            add_title("8. FDT - Teste dos Cinco Dígitos")
            add_text(sections.get("fdt", sections.get("funcoes_executivas", "")))
            add_table(
                "TABELA FDT- PROCESSOS AUTOMÁTICOS E CONTROLADOS",
                cls._fdt_rows(tests.get("fdt")),
                "fdt",
            )
            add_chart(
                "FDT - Processos Automático",
                cls._fdt_chart(tests.get("fdt"), automatic=True),
            )
            add_chart(
                "FDT - Processos Controlados",
                cls._fdt_chart(tests.get("fdt"), automatic=False),
            )

            if tests.get("etdah_pais"):
                add_title("9. E-TDAH-PAIS")
                add_text(
                    section_or_test_interpretation(
                        "etdah_pais", None, tests.get("etdah_pais")
                    )
                )
                add_table(
                    "Resultados do E-TDAH-PAIS",
                    cls._etdah_rows(tests.get("etdah_pais")),
                    "etdah",
                )
                add_chart(
                    "E-TDAH-PAIS Resultados",
                    cls._etdah_chart(tests.get("etdah_pais")),
                )

            if tests.get("etdah_ad"):
                add_title("10. E-TDAH-AD")
                add_text(
                    section_or_test_interpretation(
                        "etdah_ad", None, tests.get("etdah_ad")
                    )
                )
                add_table(
                    "Resultados do E-TDAH-AD",
                    cls._etdah_rows(tests.get("etdah_ad")),
                    "etdah",
                )
                add_chart("E-TDAH-AD Resultados", cls._etdah_chart(tests.get("etdah_ad")))

            scared_tests = cls._find_tests(context, "scared")
            if scared_tests:
                add_title("11. SCARED")
                add_text(
                    section_or_test_interpretation(
                        "scared", None, scared_tests[0]
                    )
                )
                for scared_test in scared_tests:
                    form_label = cls._scared_form_label(scared_test)
                    add_table(
                        f"SCARED - Resultados {form_label}",
                        cls._scared_rows(scared_test),
                        "scared"
                    )
                    add_chart(
                        f"SCARED Resultados {form_label}",
                        cls._scared_chart(scared_test),
                    )

            if tests.get("epq_j"):
                add_title("12. EPQ-J")
                add_text(
                    section_or_test_interpretation(
                        "epq_j", None, tests.get("epq_j")
                    )
                )
                add_table(
                    "EPQ-J Resultados da personalidade",
                    cls._epq_rows(tests.get("epq_j")),
                    "epq",
                )
                add_chart(
                    "EPQ-J Resultados dos percentis",
                    cls._epq_chart(tests.get("epq_j")),
                )

            if tests.get("srs2"):
                srs2_test = tests.get("srs2")
                add_title("13. SRS-2 Escala de Responsividade Social")
                add_text(
                    section_or_test_interpretation(
                        "srs2", None, srs2_test
                    )
                )
                add_table("SRS-2 Resultados", cls._srs2_rows(srs2_test), "srs2")
                add_chart("SRS-2 Resultados", cls._srs2_chart(srs2_test))
        else:
            add_title("5.1. Atenção")
            add_text(sections.get("atencao", ""))
            add_table("Atenção BPA-2 Resultados", cls._bpa_rows(tests.get("bpa2"), context), "bpa")
            add_chart(
                "BPA-2 apresenta os resultados da avaliação da atenção",
                cls._bpa_chart_bytes(tests.get("bpa2")),
            )

            add_title("5.2. Memória e Aprendizagem")
            add_text(sections.get("memoria_aprendizagem", ""))
            add_table(
                cls._ravlt_table_caption(), cls._ravlt_rows(tests.get("ravlt"), context), "ravlt"
            )
            add_chart("RAVLT Resultados", cls._ravlt_chart(tests.get("ravlt")))

            add_title("5.3. Funções Executivas")
            add_text(sections.get("funcoes_executivas", ""))
            add_table(
                "TABELA FDT- PROCESSOS AUTOMÁTICOS E CONTROLADOS",
                cls._fdt_rows(tests.get("fdt")),
                "fdt",
            )
            add_chart(
                "FDT - Processos Automático",
                cls._fdt_chart(tests.get("fdt"), automatic=True),
            )
            add_chart(
                "FDT - Processos Controlados",
                cls._fdt_chart(tests.get("fdt"), automatic=False),
            )

            add_title("5.4. Aspectos Emocionais, Comportamentais e Escalas Complementares")
            add_text(sections.get("aspectos_emocionais_comportamentais", ""))
            add_table(
                "E-TDAH Resultados",
                cls._etdah_rows(tests.get("etdah_ad") or tests.get("etdah_pais")),
                "etdah",
            )
            add_chart(
                "E-TDAH Resultados",
                cls._etdah_chart(tests.get("etdah_ad") or tests.get("etdah_pais")),
            )
            for scared_test in cls._find_tests(context, "scared"):
                form_label = cls._scared_form_label(scared_test)
                add_table(
                    f"SCARED - Resultados {form_label}",
                    cls._scared_rows(scared_test),
                    "scared"
                )
                add_chart(
                    f"SCARED Resultados {form_label}",
                    cls._scared_chart(scared_test),
                )
            add_table(
                "EPQ-J Resultados da personalidade",
                cls._epq_rows(tests.get("epq_j")),
                "epq",
            )
            add_chart(
                "EPQ-J Resultados dos percentis",
                cls._epq_chart(tests.get("epq_j")),
            )
            add_table("SRS-2 Resultados", cls._srs2_rows(tests.get("srs2")), "srs2")
            add_chart("SRS-2 Resultados", cls._srs2_chart(tests.get("srs2")))
            add_table(
                "Resultados da EBADEP",
                cls._ebadep_rows(
                    tests.get("ebadep_a")
                    or tests.get("ebadep_ij")
                    or tests.get("ebaped_ij")
                ),
                "scale_summary",
            )

    @classmethod
    def _find_paragraph(cls, document: Document, text: str | None):
        if not text:
            return None
        for paragraph in document.paragraphs:
            if paragraph.text.strip() == text:
                return paragraph
        return None

    @classmethod
    def _remove_nodes_between(cls, start_paragraph, end_paragraph):
        current = start_paragraph._p.getnext()
        end_element = end_paragraph._p if end_paragraph is not None else None
        while current is not None and current is not end_element:
            nxt = current.getnext()
            current.getparent().remove(current)
            current = nxt

    @classmethod
    def _insert_paragraph_after(cls, paragraph, text: str):
        new_p = OxmlElement("w:p")
        paragraph._p.addnext(new_p)
        new_paragraph = Paragraph(new_p, paragraph._parent)
        if text is not None:
            new_paragraph.add_run(text)
        return new_paragraph

    @classmethod
    def _insert_table_after(cls, paragraph, rows: list[list[str]], table_key: str | None = None):
        parent = paragraph._parent
        table_rows = cls._with_table_title(rows, table_key)
        table = parent.add_table(rows=0, cols=len(table_rows[0]), width=cls.DEFAULT_TABLE_WIDTH)
        tbl = table._tbl
        tbl.getparent().remove(tbl)
        paragraph._p.addnext(tbl)
        for row_values in table_rows:
            row = table.add_row().cells
            for index, value in enumerate(row_values):
                row[index].text = value
        return Table(tbl, parent)

    @classmethod
    def _insert_ravlt_table_after(cls, paragraph, rows: list[list[str]]):
        table = cls._insert_table_after(paragraph, rows, "ravlt")
        cls._format_ravlt_table(table)
        return table

    @classmethod
    def _with_table_title(cls, rows: list[list[str]] | None, table_key: str | None):
        if not rows or not table_key:
            return rows
        title = cls._table_title_text(table_key)
        if not title:
            return rows
        return [[title, *([""] * (len(rows[0]) - 1))], *rows]

    @classmethod
    def _table_title_text(cls, table_key: str) -> str | None:
        return {
            "bpa": "BPA-2",
            "fdt": "FDT - TESTE DOS CINCO DÍGITOS",
            "etdah": "E-TDAH-PAIS",
            "scared": "SCARED",
            "epq": "EPQ-J",
            "srs2": "SRS-2",
        }.get(table_key)

    @classmethod
    def _merge_title_row(cls, row):
        merged_text = row.cells[0].text.strip()
        merged = row.cells[0]
        for idx in range(1, len(row.cells)):
            merged = merged.merge(row.cells[idx])
        merged.text = merged_text

    @classmethod
    def _insert_paragraph_after_table(cls, table, text: str):
        new_p = OxmlElement("w:p")
        table._tbl.addnext(new_p)
        paragraph = Paragraph(new_p, table._parent)
        if text is not None:
            paragraph.add_run(text)
        return paragraph

    @classmethod
    def _clear_document_body(cls, document: Document):
        body = document._body._element
        for child in list(body):
            if child.tag.endswith("sectPr"):
                continue
            body.remove(child)

    @classmethod
    def _format_body_paragraph(cls, paragraph):
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = cls.BODY_SPACE_AFTER
        paragraph.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
        paragraph.paragraph_format.first_line_indent = cls.BODY_FIRST_LINE_INDENT
        for run in paragraph.runs:
            run.font.name = cls.FONT_NAME
            run.font.size = cls.BODY_SIZE

    @classmethod
    def _format_left_body_paragraph(cls, paragraph):
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = cls.BODY_SPACE_AFTER
        paragraph.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
        paragraph.paragraph_format.first_line_indent = cls.BODY_FIRST_LINE_INDENT
        for run in paragraph.runs:
            run.font.name = cls.FONT_NAME
            run.font.size = cls.BODY_SIZE

    @classmethod
    def _append_body_text_with_bold_label(cls, paragraph, text: str):
        stripped = text.lstrip()
        leading = text[: len(text) - len(stripped)]

        if leading:
            run = paragraph.add_run(leading)
            run.font.name = cls.FONT_NAME
            run.font.size = cls.BODY_SIZE

        for label in cls.INTERPRETATION_LABELS:
            if stripped.casefold().startswith(label.casefold()):
                bold_run = paragraph.add_run(stripped[: len(label)])
                bold_run.font.name = cls.FONT_NAME
                bold_run.font.size = cls.BODY_SIZE
                bold_run.bold = True

                remainder = stripped[len(label) :]
                if remainder:
                    run = paragraph.add_run(remainder)
                    run.font.name = cls.FONT_NAME
                    run.font.size = cls.BODY_SIZE
                return

        run = paragraph.add_run(stripped)
        run.font.name = cls.FONT_NAME
        run.font.size = cls.BODY_SIZE

    @classmethod
    def _append_wisc_intro_paragraph(cls, paragraph, text: str):
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = cls.BODY_SPACE_AFTER
        paragraph.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
        paragraph.paragraph_format.first_line_indent = cls.BODY_FIRST_LINE_INDENT

        qit_match = re.search(r"QI Total \(QIT [^)]+\)", text)
        class_match = re.search(r"ficando na classificação ([^,.]+)", text)
        age_phrase_match = re.search(
            r"quando comparado à média geral e com idade cognitiva estimada de [^.]+",
            text,
        )

        bold_segments = [
            "Capacidade Cognitiva Global:",
            "WISC IV",
        ]
        if qit_match:
            bold_segments.append(qit_match.group(0))
        if class_match:
            bold_segments.append(class_match.group(1).strip())
        if age_phrase_match:
            bold_segments.append(age_phrase_match.group(0))

        cursor = 0
        for segment in sorted(set(bold_segments), key=lambda item: text.find(item)):
            index = text.find(segment, cursor)
            if index < 0:
                continue
            if index > cursor:
                run = paragraph.add_run(text[cursor:index])
                run.font.name = cls.FONT_NAME
                run.font.size = cls.BODY_SIZE
            run = paragraph.add_run(segment)
            run.font.name = cls.FONT_NAME
            run.font.size = cls.BODY_SIZE
            run.bold = True
            cursor = index + len(segment)

        if cursor < len(text):
            run = paragraph.add_run(text[cursor:])
            run.font.name = cls.FONT_NAME
            run.font.size = cls.BODY_SIZE

    @staticmethod
    def _wisc_payload(test: dict | None) -> dict:
        return (
            (test or {}).get("structured_results")
            or (test or {}).get("classified_payload")
            or (test or {}).get("computed_payload")
            or {}
        )

    @classmethod
    def _wisc_global_intro_text(cls, test: dict | None, context: dict) -> str:
        payload = cls._wisc_payload(test)
        qit = payload.get("qit_data") or {}
        patient_label = "A paciente" if (context.get("patient") or {}).get("sex") == "F" else "O paciente"
        intro = (
            f"Capacidade Cognitiva Global: {patient_label} obteve, a partir da escala WISC IV, "
            f"QI Total (QIT {qit.get('escore_composto', 'não informado')}), ficando na classificação "
            f"{qit.get('classificacao', 'não informada')}"
        )
        idade_cognitiva = payload.get("idade_cognitiva")
        if idade_cognitiva:
            intro += (
                f", quando comparado à média geral e com idade cognitiva estimada de {idade_cognitiva}"
            )
        intro += ". Em relação aos índices fatoriais (medidas mais apuradas da inteligência), apresentou os seguintes resultados:"
        return intro

    @classmethod
    def _wisc_global_bullet_parts(cls, test: dict | None) -> list[tuple[str, str]]:
        payload = cls._wisc_payload(test)
        indices = {item.get("indice"): item for item in payload.get("indices") or []}
        definitions = [
            ("Compreensão Verbal", "ICV", indices.get("icv"), "Avaliou o conhecimento verbal adquirido, o processo mental necessário para responder às questões formuladas, a capacidade de compreensão verbal e o raciocínio verbal."),
            ("Organização Perceptual", "IOP", indices.get("iop"), "Avaliou o raciocínio não verbal, a atenção para detalhes e a integração visomotora."),
            ("Memória Operacional", "IMO", indices.get("imt"), "Avaliou a atenção, a concentração e a memória operacional."),
            ("Velocidade de Processamento", "IVP", indices.get("ivp"), "Avaliou a capacidade de em realizar tarefas que demandam rapidez e precisão na análise de estímulos visuais."),
        ]
        rows: list[tuple[str, str]] = []
        for label, code, item, description in definitions:
            item = item or {}
            lead = (
                f"{label} ({code}) — {item.get('escore_composto', 'não informado')} — "
                f"{item.get('classificacao', 'não informada')}"
            )
            rows.append((lead, description))
        return rows

    @classmethod
    def _append_wisc_global_bullet(cls, paragraph, lead: str, tail: str):
        bullet_prefix = paragraph.add_run("-\t")
        bullet_prefix.font.name = cls.FONT_NAME
        bullet_prefix.font.size = cls.BODY_SIZE
        bold_run = paragraph.add_run(lead)
        bold_run.font.name = cls.FONT_NAME
        bold_run.font.size = cls.BODY_SIZE
        bold_run.bold = True
        tail_run = paragraph.add_run(f" {tail}")
        tail_run.font.name = cls.FONT_NAME
        tail_run.font.size = cls.BODY_SIZE
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = cls.BODY_SPACE_AFTER
        paragraph.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
        paragraph.paragraph_format.left_indent = Cm(1.1)
        paragraph.paragraph_format.first_line_indent = Cm(-0.55)
        paragraph.paragraph_format.tab_stops.add_tab_stop(Cm(1.1))

    @classmethod
    def _append_wisc_global_block(cls, document, test: dict | None, context: dict):
        intro = cls._wisc_global_intro_text(test, context)
        p = document.add_paragraph()
        cls._append_wisc_intro_paragraph(p, intro)
        for lead, tail in cls._wisc_global_bullet_parts(test):
            p = document.add_paragraph()
            cls._append_wisc_global_bullet(p, lead, tail)

    @classmethod
    def _format_subtitle_paragraph(cls, paragraph):
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        paragraph.paragraph_format.space_before = cls.SUBHEADING_SPACE_BEFORE
        paragraph.paragraph_format.space_after = cls.SUBHEADING_SPACE_AFTER
        paragraph.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
        paragraph.paragraph_format.keep_with_next = True
        paragraph.paragraph_format.first_line_indent = Pt(0)
        for run in paragraph.runs:
            run.font.name = cls.FONT_NAME
            run.font.size = cls.TITLE_SIZE
            run.bold = True

    @classmethod
    def _format_caption_paragraph(cls, paragraph):
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.paragraph_format.space_before = Pt(4)
        paragraph.paragraph_format.space_after = Pt(3)
        paragraph.paragraph_format.line_spacing = 1.0
        paragraph.paragraph_format.keep_with_next = True
        for run in paragraph.runs:
            run.font.name = cls.FONT_NAME
            run.font.size = cls.CAPTION_SIZE
            run.italic = True

    @classmethod
    def _table_caption_text(cls, table_index: int, caption: str) -> str:
        return f"Tabela {table_index} {caption}"

    @classmethod
    def _chart_caption_text(cls, chart_index: int, caption: str) -> str:
        return f"Gráfico {chart_index} {caption}"

    @classmethod
    def _ravlt_table_caption(cls) -> str:
        return (
            'RAVLT Resultados: referente ao desempenho do paciente durante a prova RAVLT '
            '(memória auditiva e aprendizagem de palavras). Os intervalos "A" se referem '
            'à exposição de uma mesma lista de palavras e ao desempenho da memória de curto '
            'prazo. O intervalo "B1" se refere à intrusão de uma nova lista de palavras.'
        )

    @classmethod
    def _add_center_title(cls, document, text: str):
        p = document.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.font.name = cls.FONT_NAME
        r.font.size = cls.TITLE_SIZE
        r.bold = True
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = cls.HEADING_SPACE_AFTER
        p.paragraph_format.line_spacing = cls.IDENTIFICATION_LINE_SPACING

    @classmethod
    def _add_center_text(cls, document, text: str):
        p = document.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.font.name = cls.FONT_NAME
        r.font.size = cls.CAPTION_SIZE
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = cls.IDENTIFICATION_LINE_SPACING

    @classmethod
    def _append_heading(cls, document, text: str):
        p = document.add_paragraph()
        if text.endswith("EFICIÊNCIA COGNITIVA") and ". " in text:
            number, heading_text = text.split(". ", 1)
            runs = [
                p.add_run(f"{number}."),
                p.add_run("\t\t"),
                p.add_run(heading_text),
            ]
        else:
            runs = [p.add_run(text)]
        for run in runs:
            run.font.name = cls.FONT_NAME
            run.font.size = cls.TITLE_SIZE
            run.bold = True
        p.paragraph_format.space_before = cls.HEADING_SPACE_BEFORE
        p.paragraph_format.space_after = cls.HEADING_SPACE_AFTER
        p.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
        p.paragraph_format.first_line_indent = Pt(0)

    @classmethod
    def _append_subheading(cls, document, text: str):
        text = PtBrTextService.normalize(text)
        p = document.add_paragraph()
        r = p.add_run(text)
        r.font.name = cls.FONT_NAME
        r.font.size = cls.TITLE_SIZE
        r.bold = True
        p.paragraph_format.space_before = cls.SUBHEADING_SPACE_BEFORE
        p.paragraph_format.space_after = cls.SUBHEADING_SPACE_AFTER
        p.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
        p.paragraph_format.first_line_indent = Pt(0)

    @classmethod
    def _append_paragraph(cls, document, text: str, center: bool = False):
        text = PtBrTextService.normalize(text)
        if not text:
            return
        p = document.add_paragraph()
        p.alignment = (
            WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.JUSTIFY
        )
        cls._append_body_text_with_bold_label(p, text)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = cls.BODY_SPACE_AFTER
        p.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
        p.paragraph_format.first_line_indent = Pt(0) if center else cls.BODY_FIRST_LINE_INDENT

    @classmethod
    def _append_identification_text(cls, document, text: str):
        text = PtBrTextService.normalize(text)
        p = document.add_paragraph()
        r = p.add_run(text)
        r.font.name = cls.FONT_NAME
        r.font.size = cls.BODY_SIZE
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = cls.IDENTIFICATION_LINE_SPACING
        p.paragraph_format.first_line_indent = Pt(0)

    @classmethod
    def _append_label_value(cls, document, label: str, value: str):
        label = PtBrTextService.normalize(label)
        value = PtBrTextService.normalize(str(value or "Não informado"))
        p = document.add_paragraph()
        a = p.add_run(f"{label}: ")
        a.font.name = cls.FONT_NAME
        a.font.size = cls.BODY_SIZE
        a.bold = True
        b = p.add_run(value)
        b.font.name = cls.FONT_NAME
        b.font.size = cls.BODY_SIZE
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = cls.IDENTIFICATION_LINE_SPACING
        p.paragraph_format.first_line_indent = Pt(0)

    @classmethod
    def _append_bullet(cls, document, text: str):
        text = PtBrTextService.normalize(text)
        try:
            p = document.add_paragraph(style="List Bullet")
            r = p.add_run(text)
        except KeyError:
            p = document.add_paragraph()
            r = p.add_run(f"• {text}")
        r.font.name = cls.FONT_NAME
        r.font.size = cls.BODY_SIZE
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = cls.BODY_SPACE_AFTER
        p.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
        p.paragraph_format.left_indent = Cm(0.75)
        p.paragraph_format.first_line_indent = Cm(-0.25)

    @classmethod
    def _append_numbered_item(cls, document, text: str):
        text = PtBrTextService.normalize(text)
        p = document.add_paragraph()
        r = p.add_run(text)
        r.font.name = cls.FONT_NAME
        r.font.size = cls.BODY_SIZE
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = cls.BODY_SPACE_AFTER
        p.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
        p.paragraph_format.left_indent = Cm(0.75)
        p.paragraph_format.first_line_indent = Cm(-0.25)

    @classmethod
    def _append_table_with_interpretation(
        cls,
        document,
        rows,
        table_key: str,
        interpretation: str | None,
        caption: str | None = None,
    ):
        if rows:
            table_rows = cls._with_table_title(rows, table_key)
            table = document.add_table(rows=0, cols=len(table_rows[0]))
            for row_values in table_rows:
                row = table.add_row().cells
                for idx, value in enumerate(row_values):
                    row[idx].text = str(value)
            if table_key == "ravlt":
                cls._format_ravlt_table(table)
            else:
                cls._format_table(table, table_key)
            if caption:
                caption_paragraph = document.add_paragraph()
                caption_run = caption_paragraph.add_run(caption)
                caption_run.font.name = cls.FONT_NAME
                caption_run.font.size = Pt(10)
                caption_run.italic = True
                cls._format_caption_paragraph(caption_paragraph)
        if interpretation:
            cls._append_interpretation_block(
                document, cls._normalize_interpretation_text(interpretation)
            )

    @classmethod
    def _append_interpretation_block(cls, document, text: str):
        cleaned = (text or "").strip()
        if not cleaned:
            return

        paragraphs = [
            item.strip()
            for item in re.split(r"\n\s*\n+", cleaned)
            if item.strip()
        ]

        for item in paragraphs:
            p = document.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            cls._append_body_text_with_bold_label(p, item)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
            p.paragraph_format.first_line_indent = Pt(0)

    @classmethod
    def _append_ravlt_conceptual_paragraph(cls, document):
        text = cls._ravlt_conceptual_text()
        if not text:
            return
        p = document.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(text)
        r.font.name = cls.FONT_NAME
        r.font.size = Pt(10)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.first_line_indent = Pt(0)

    @classmethod
    def _insert_ravlt_conceptual_paragraph_after(cls, anchor):
        anchor = cls._insert_paragraph_after(anchor, cls._ravlt_conceptual_text())
        anchor.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        anchor.paragraph_format.space_before = Pt(0)
        anchor.paragraph_format.space_after = Pt(0)
        anchor.paragraph_format.line_spacing = 1.15
        anchor.paragraph_format.first_line_indent = Pt(0)
        for run in anchor.runs:
            run.font.name = cls.FONT_NAME
            run.font.size = Pt(10)
        return anchor

    @classmethod
    def _insert_interpretation_block_after(cls, anchor, text: str):
        cleaned = (text or "").strip()
        if not cleaned:
            return anchor
        paragraphs = [
            item.strip()
            for item in re.split(r"\n\s*\n+", cleaned)
            if item.strip()
        ]
        for item in paragraphs:
            anchor = cls._insert_paragraph_after(anchor, "")
            cls._append_body_text_with_bold_label(anchor, item)
            anchor.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            anchor.paragraph_format.space_before = Pt(0)
            anchor.paragraph_format.space_after = Pt(0)
            anchor.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
            anchor.paragraph_format.first_line_indent = Pt(0)
        return anchor

    @classmethod
    def _normalize_interpretation_text(cls, interpretation: str) -> str:
        label = "Interpretação e Observações Clínicas:"
        text = PtBrTextService.normalize(cls._strip_legacy_srs2_table(interpretation))
        if not text:
            return label
        if text.casefold().startswith(label.casefold()):
            return text
        return f"{label} {text}"

    @classmethod
    def _strip_legacy_srs2_table(cls, text: str | None) -> str:
        cleaned = (text or "").strip()
        if not cleaned:
            return ""

        cleaned = re.sub(
            r"={20,}\s*\n"
            r"Fator\s+Pts\s*Brts\s+T-Score\s+Percentil\s+Classifica(?:ç|c)ão\s*\n"
            r"={20,}\s*\n"
            r".*?"
            r"\n={20,}",
            "",
            cleaned,
            flags=re.IGNORECASE | re.DOTALL,
        ).strip()

        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        if cleaned in cls.EMPTY_INTERPRETATION_MESSAGES:
            return ""
        return cleaned

    @classmethod
    def _resolve_interpretation_text(
        cls,
        primary_section: str | None,
        fallback_section: str | None,
        test_payload: dict | None,
    ) -> str:
        candidates = [
            primary_section,
            fallback_section,
            (test_payload or {}).get("clinical_interpretation"),
            (test_payload or {}).get("summary"),
            cls._fallback_test_interpretation(test_payload),
        ]

        for candidate in candidates:
            cleaned = cls._strip_legacy_srs2_table(candidate)
            if cleaned:
                return cleaned
        return ""

    @classmethod
    def _merge_text_blocks(cls, *blocks: str | None) -> str:
        cleaned_blocks = []
        seen = set()
        for block in blocks:
            cleaned = PtBrTextService.normalize(block)
            if not cleaned:
                continue
            key = cleaned.casefold()
            if key in seen:
                continue
            seen.add(key)
            cleaned_blocks.append(cleaned)
        return "\n\n".join(cleaned_blocks)

    @classmethod
    def _fallback_test_interpretation(cls, test_payload: dict | None) -> str:
        if not test_payload or test_payload.get("instrument_code") != "srs2":
            return ""

        merged_data = {
            **(test_payload.get("computed_payload") or {}),
            **(
                test_payload.get("classified_payload")
                or test_payload.get("structured_results")
                or {}
            ),
        }
        return (interpret_srs2_results(merged_data) or "").strip()

    @classmethod
    def _ravlt_conceptual_text(cls) -> str:
        return (
            "O Rey Auditory Verbal Learning Test (RAVLT) é um teste neuropsicológico amplamente utilizado para avaliar a memória verbal, a capacidade de aprendizado auditivo e a retenção de informações ao longo do tempo. Desenvolvido por Rey (1958). O RAVLT permite analisar diferentes aspectos da memória, como a curva de aprendizado, interferência, esquecimento e reconhecimento verbal (Lezak et al., 2004). Ele é frequentemente utilizado na investigação de déficits cognitivos associados a doenças neurodegenerativas, lesões cerebrais traumáticas e transtornos psiquiátricos (Strauss, Sherman & Spreen, 2006). Os resultados do teste auxiliam no diagnóstico diferencial de condições como Alzheimer e TDAH, além de fornecerem subsídios para o planejamento de intervenções cognitivas (Salthouse, 2010). Assim, o RAVLT é uma ferramenta essencial para a avaliação da memória e da aprendizagem verbal."
        )

    @classmethod
    def _append_chart(cls, document, caption: str | None, image_bytes: bytes | None, width=None):
        if not image_bytes:
            return
        img = document.add_paragraph()
        img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img.add_run().add_picture(BytesIO(image_bytes), width=width or cls.IMAGE_WIDTH)
        if caption:
            p = document.add_paragraph()
            r = p.add_run(caption)
            r.font.name = cls.FONT_NAME
            r.font.size = cls.BODY_SIZE
            cls._format_caption_paragraph(p)

    @classmethod
    def _format_chart_legend_paragraph(cls, paragraph):
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = cls.BODY_SPACE_AFTER
        paragraph.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
        paragraph.paragraph_format.first_line_indent = Pt(0)
        for run in paragraph.runs:
            run.font.name = cls.FONT_NAME
            run.font.size = cls.CAPTION_SIZE
            run.font.color.rgb = RGBColor(0x5B, 0x9B, 0xD5)
            run.bold = False
            run.italic = True

    @classmethod
    def _wisc_chart_legend(cls, chart_index: int) -> str:
        return (
            f"Gráfico {chart_index} WISC-IV - INDICES DE QIS :"
            "Índice de Compreensão Verbal (ICV): composto por provas que avaliam as habilidades verbais por meio do raciocínio, compreensão e conceituação. "
            "Índice de Organização Perceptual (IOP): constituído por atividades que examinam o grau e a qualidade do contato não verbal do indivíduo com o ambiente, assim como a capacidade de integrar estímulos perceptuais e respostas motoras pertinentes, o nível de rapidez com o qual executa uma atividade e o modo como avalia informações visuoespaciais. "
            "Índice de Memória Operacional (IMO): formado por provas que analisam atenção, concentração e memória de trabalho. "
            "Índice de Velocidade de Processamento (IVP): constitui-se de atividades que avaliam agilidade mental e processamento grafomotor. "
            "Coeficiente de Inteligência Total (QIT): avalia o nível geral do funcionamento intelectual."
        )

    @classmethod
    def _find_test(cls, context: dict, code: str):
        for item in context.get("validated_tests") or []:
            if item.get("instrument_code") == code:
                return item
        return None

    @classmethod
    def _find_tests(cls, context: dict, code: str):
        tests = [
            item
            for item in context.get("validated_tests") or []
            if item.get("instrument_code") == code
        ]
        form_order = {"child": 0, "parent": 1}
        return sorted(
            tests,
            key=lambda item: form_order.get(
                ((item.get("classified_payload") or {}).get("form_type") or (item.get("raw_payload") or {}).get("form") or "child"),
                99,
            ),
        )

    @staticmethod
    def _scared_form_label(test: dict | None) -> str:
        form_type = ((test or {}).get("classified_payload") or {}).get("form_type") or ((test or {}).get("raw_payload") or {}).get("form")
        return "Pais/Cuidadores" if form_type == "parent" else "Autorrelato"

    @classmethod
    def _format_date_display(cls, value: str | None) -> str:
        if not value:
            return "Não informado"
        try:
            year, month, day = value.split("-")
            return f"{day}/{month}/{year}"
        except ValueError:
            return value

    @staticmethod
    def _format_sex_display(value: str | None) -> str:
        return {"M": "Masculino", "F": "Feminino", "O": "Outro"}.get(
            value or "", value or "Não informado"
        )

    @classmethod
    def _age_text(cls, context: dict) -> str:
        birth_date = (context.get("patient") or {}).get("birth_date")
        if not birth_date:
            return "Não informada"
        try:
            from datetime import date

            year, month, day = map(int, birth_date.split("-"))
            born = date(year, month, day)
            today = date.today()
            years = (
                today.year
                - born.year
                - ((today.month, today.day) < (born.month, born.day))
            )
            months = (today.month - born.month) % 12
            return f"{years} anos e {months} meses"
        except ValueError:
            return "Não informada"

    @staticmethod
    def _filiation_text(patient: dict) -> str:
        names = [patient.get("father_name"), patient.get("mother_name")]
        names = [name for name in names if name]
        return (
            " e ".join(names)
            if names
            else patient.get("responsible_name") or "Não informada"
        )

    @staticmethod
    def _schooling_text(patient: dict) -> str:
        return patient.get("grade_year") or patient.get("schooling") or "Não informada"

    @classmethod
    def _procedures_intro(cls, context: dict) -> str:
        sessions = len(context.get("progress_entries") or []) or 5
        age_text = cls._age_text(context)
        subject = "paciente"
        if age_text != "Não informada":
            try:
                years = int(str(age_text).split(" ", 1)[0])
                if years < 12:
                    subject = "criança"
                elif years < 18:
                    subject = "adolescente"
                else:
                    subject = "paciente"
            except (TypeError, ValueError):
                subject = "paciente"
        return f"Para esta avaliação foram realizadas: uma sessão de anamnese, {sessions:02d} sessões de testagem com o(a) {subject} e uma sessão de devolutiva com familiar responsável."

    @classmethod
    def _adolescent_instruments(cls, context: dict):
        validated_codes = []
        seen_codes = {"anamnese"}
        for test in context.get("validated_tests") or []:
            code = test.get("instrument_code")
            if not code or code in seen_codes:
                continue
            seen_codes.add(code)
            validated_codes.append(code)

        ordered_codes = [
            code
            for code in cls.PROCEDURES_ORDER
            if code == "anamnese" or code in validated_codes
        ]

        items = []
        for code in ordered_codes:
            catalog_entry = cls.INSTRUMENT_CATALOG.get(code)
            if not catalog_entry:
                continue
            items.append(
                {
                    "name": catalog_entry["nome"],
                    "description": catalog_entry["descricao"],
                }
            )

        remaining_codes = [
            code for code in validated_codes if code not in cls.PROCEDURES_ORDER
        ]
        for code in remaining_codes:
            catalog_entry = cls.INSTRUMENT_CATALOG.get(code)
            if not catalog_entry:
                continue
            items.append(
                {
                    "name": catalog_entry["nome"],
                    "description": catalog_entry["descricao"],
                }
            )

        return items

    @staticmethod
    def _split_bullets(text: str):
        if not text:
            return []
        parts = [part.strip(" -") for part in text.split("\n") if part.strip()]
        return parts or [text]

    @classmethod
    def _team_paragraphs(cls, report):
        email = getattr(getattr(report, "author", None), "email", "") or ""
        return [
            "A Avaliação Neuropsicológica, quando bem fundamentada, é essencial para direcionar a reabilitação cognitiva e fornecer subsídios para outros profissionais em suas respectivas áreas de atuação.",
            "É importante que o documento seja lido na íntegra, e não apenas a conclusão, para que se compreenda plenamente o raciocínio clínico utilizado ao longo de todo o processo avaliativo.",
            f"Com a devida autorização por escrito dos responsáveis, coloco-me à disposição para esclarecimentos e discussões sobre o exame{f', podendo ser contatada pelo e-mail {email}' if email else ''}.",
        ]

    @classmethod
    def _important_document_items(cls):
        return [
            "1. Não deve ser utilizado para fins diferentes daqueles especificados no item de identificação do documento.",
            "2. Possui caráter sigiloso e extrajudicial, não cabendo à psicóloga a responsabilidade pelo seu uso indevido ou pela entrega do laudo sem autorização adequada.",
            "3. A análise isolada deste laudo não possui valor diagnóstico se não for considerada em conjunto com dados clínicos, epistemológicos, exames de neuroimagem e laboratoriais adicionais referentes ao paciente.",
            "4. Esta avaliação está em conformidade com as Resoluções CRP 09/2018 e 06/2019. Em conformidade com o Código de Ética Profissional, este exame deve ser tratado como confidencial.",
        ]

    @classmethod
    def _signature_lines(cls, report):
        author_name = getattr(
            getattr(report, "author", None), "display_name", "Profissional responsável"
        )
        created = getattr(report, "created_at", None)
        city = "Goiânia"
        date_text = created.strftime("%d/%m/%Y") if created else ""
        return [f"{city}, {date_text}", "", author_name]

    @staticmethod
    def _references_list(context: dict):
        return build_references(context.get("validated_tests") or [])

    @classmethod
    def _wisc_memory_rows(cls, test: dict | None, context: dict):
        payload = (test or {}).get("classified_payload") or {}
        ncp_table = cls._wisc_ncp_table(context)
        rows = [[
            "Testes Utilizados",
            "Escore Máximo",
            "Escore Médio",
            "Escore Mínimo",
            "Escore Bruto",
            "Classificação",
        ]]
        labels = {
            "SNL": "Seq. Núm. e Letras",
            "DG": "Dígitos",
        }
        for code in ("SNL", "DG"):
            item = next(
                (entry for entry in payload.get("subtestes") or [] if entry.get("codigo") == code),
                None,
            )
            if not item:
                continue
            score_max, score_mid, score_min = cls._wisc_reference_scores(
                ncp_table, code
            )
            rows.append(
                [
                    labels.get(code, item.get("subteste") or "-"),
                    score_max,
                    score_mid,
                    score_min,
                    cls._num(item.get("escore_bruto")),
                    item.get("classificacao") or "-",
                ]
            )
        return rows if len(rows) > 1 else None

    @classmethod
    def _ravlt_norm_band(cls, test: dict | None, context: dict | None = None) -> str:
        context = context or {}
        patient = context.get("patient") or {}
        birth_date = patient.get("birth_date")
        applied_on = (test or {}).get("applied_on")
        if birth_date and applied_on:
            try:
                age = _calcular_idade(str(birth_date), str(applied_on)[:10])
                if isinstance(age, tuple):
                    age = age[0]
                return get_ravlt_age_band(int(age))
            except Exception:
                pass

        payload = (test or {}).get("classified_payload") or {}
        band = payload.get("faixa_etaria")
        if band in RAVLT_NORMS:
            return band
        return "21-30"

    @classmethod
    def _ravlt_obtained_map(cls, test: dict | None) -> dict:
        classified = (test or {}).get("classified_payload") or {}
        computed = (test or {}).get("computed_payload") or {}
        # Build a normalized map from classified resultados for flexible key matching
        def _normalize_key(s: str | None) -> str | None:
            if not s:
                return None
            # lower-case and keep only ascii alphanumerics
            return re.sub(r"[^a-z0-9]", "", str(s).casefold())

        results_map = {}
        for item in classified.get("resultados") or []:
            if not isinstance(item, dict):
                continue
            var = item.get("variavel") or item.get("variavel_nome") or item.get("nome")
            key = _normalize_key(var) or None
            if key:
                results_map[key] = item

        def _get_bruto_from_results(names: list[str]) -> object:
            for name in names:
                key = _normalize_key(name)
                if key and key in results_map:
                    return results_map[key].get("bruto")
            return None

        # Try to read values from the classified resultados if available
        if results_map:
            return {
                "A1": _get_bruto_from_results(["A1", "a1"]),
                "A2": _get_bruto_from_results(["A2", "a2"]),
                "A3": _get_bruto_from_results(["A3", "a3"]),
                "A4": _get_bruto_from_results(["A4", "a4"]),
                "A5": _get_bruto_from_results(["A5", "a5"]),
                "B1": _get_bruto_from_results(["B1", "b1", "b"]),
                "A6": _get_bruto_from_results(["A6", "a6"]),
                "A7": _get_bruto_from_results(["A7", "a7"]),
                "R": _get_bruto_from_results(["R", "r", "reconhecimentolistaa", "reconhecimento lista a"]),
                "ALT": _get_bruto_from_results(["ALT", "alt", "aprendlongodastentativas", "aprend longo das tentativas"]),
                "RET": _get_bruto_from_results(["RET", "ret", "velocidadedeesquecimento", "velocidade de esquecimento"]),
                "I.P.": _get_bruto_from_results(["IP", "ip", "interferenciaproativa", "interferência proativa"]),
                "I.R.": _get_bruto_from_results(["IR", "ir", "interferenciaretroativa", "interferência retroativa"]),
            }

        # Fallback: try to read from computed_payload or classified top-level short keys
        return {
            "A1": computed.get("a1", {}).get("escore") or classified.get("a1"),
            "A2": computed.get("a2", {}).get("escore") or classified.get("a2"),
            "A3": computed.get("a3", {}).get("escore") or classified.get("a3"),
            "A4": computed.get("a4", {}).get("escore") or classified.get("a4"),
            "A5": computed.get("a5", {}).get("escore") or classified.get("a5"),
            "B1": computed.get("b", {}).get("escore") or classified.get("b1") or classified.get("b"),
            "A6": computed.get("a6", {}).get("escore") or classified.get("a6"),
            "A7": computed.get("a7", {}).get("escore") or classified.get("a7"),
            "R": computed.get("reconhecimento", {}).get("escore") or classified.get("r"),
            "ALT": computed.get("aprend_longo", {}).get("escore") or classified.get("alt"),
            "RET": computed.get("velocidade_esquecimento", {}).get("escore") or classified.get("ret"),
            "I.P.": computed.get("interferencia_proativa", {}).get("escore") or classified.get("ip"),
            "I.R.": computed.get("interferencia_retroativa", {}).get("escore") or classified.get("ir"),
        }

    @classmethod
    def _ravlt_rows(cls, test: dict | None, context: dict | None = None):
        # Columns in the same order as the reference model.
        columns = [
            "A1",
            "A2",
            "A3",
            "A4",
            "A5",
            "B1",
            "A6",
            "A7",
            "R",
            "ALT",
            "RET",
            "I.P.",
            "I.R.",
        ]
        norm_key_map = {
            "A1": "A1",
            "A2": "A2",
            "A3": "A3",
            "A4": "A4",
            "A5": "A5",
            "A6": "A6",
            "A7": "A7",
            "B1": "B1",
            "R": "Reconhecimento Lista A",
            "ALT": "Aprend. longo das Tentativas",
            "RET": "Velocidade de Esquecimento",
            "I.P.": "Interferência Proativa",
            "I.R.": "Interferência Retroativa",
        }
        band = cls._ravlt_norm_band(test, context)
        norms = RAVLT_NORMS.get(band, RAVLT_NORMS["21-30"])

        # Prefer explicit payload values if present: ravlt_esperado / ravlt_minimo / ravlt_obtido
        payload_source = (test or {})
        classified = (test or {}).get("classified_payload") or {}
        computed = (test or {}).get("computed_payload") or {}

        # Merge likely locations for a potential ravlt payload
        candidate_payloads = [payload_source, classified, computed]

        def _find_ravlt_map(key_name: str) -> dict | None:
            for src in candidate_payloads:
                val = src.get(key_name)
                if isinstance(val, dict) and val:
                    return val
            return None

        ravlt_expected_raw = _find_ravlt_map("ravlt_esperado")
        ravlt_minimum_raw = _find_ravlt_map("ravlt_minimo")
        ravlt_obtained_raw = _find_ravlt_map("ravlt_obtido")

        def _normalize_payload_map(m: dict | None) -> dict:
            if not m:
                return {}
            mapping = {}
            short_map = {
                "a1": "A1",
                "a2": "A2",
                "a3": "A3",
                "a4": "A4",
                "a5": "A5",
                "b1": "B1",
                "b": "B1",
                "a6": "A6",
                "a7": "A7",
                "r": "R",
                "alt": "ALT",
                "ret": "RET",
                "ip": "I.P.",
                "ir": "I.R.",
            }
            for k, v in (m or {}).items():
                if not k:
                    continue
                key_norm = str(k).casefold()
                if key_norm in short_map:
                    mapping[short_map[key_norm]] = v
                else:
                    # also accept keys already matching final labels
                    mapping_key = k if k in columns else None
                    if mapping_key:
                        mapping[mapping_key] = v
            return mapping

        expected_map = _normalize_payload_map(ravlt_expected_raw)
        minimum_map = _normalize_payload_map(ravlt_minimum_raw)
        obtained_map = _normalize_payload_map(ravlt_obtained_raw)

        # If obtained_map is empty, fallback to computed/classified extraction
        if not any(v is not None for v in obtained_map.values()):
            obtained_map = cls._ravlt_obtained_map(test)

        if not any(value is not None for value in obtained_map.values()):
            return None

        # Header: first cell is the label 'Desempenho', then the numeric column labels
        rows = [["Desempenho", *columns], ["Esperado"], ["Mínimo"], ["Obtido"]]
        for column in columns:
            # Prefer explicit payload expected/minimum, otherwise use norms
            if expected_map.get(column) is not None:
                rows[1].append(cls._num(expected_map.get(column)))
            else:
                norm = norms.get(norm_key_map[column])
                rows[1].append(cls._num(norm.p50 if norm else None))

            if minimum_map.get(column) is not None:
                rows[2].append(cls._num(minimum_map.get(column)))
            else:
                norm = norms.get(norm_key_map[column])
                rows[2].append(cls._num(norm.p25 if norm else None))

            rows[3].append(cls._num(obtained_map.get(column)))
        return rows

    @classmethod
    def _format_table(cls, table, table_key: str):
        table.style = "Table Grid"
        table.alignment = (
            WD_TABLE_ALIGNMENT.LEFT if table_key in {"wisc", "bpa"} else WD_TABLE_ALIGNMENT.CENTER
        )
        table.autofit = False
        cls._apply_table_widths(table, table_key)
        title_text = cls._table_title_text(table_key)
        for row_index, row in enumerate(table.rows):
            if row_index == 0:
                cls._set_repeat_table_header(row)
            for cell_index, cell in enumerate(row.cells):
                if table_key == "wisc":
                    if row_index == 0:
                        cls._set_cell_shading(cell, cls.WISC_HEADER_FILL)
                    elif cell == row.cells[0]:
                        cls._set_cell_shading(cell, cls.WISC_NAME_FILL)
                    else:
                        cls._set_cell_shading(cell, cls.WISC_VALUE_FILL)
                elif table_key == "bpa":
                    if row_index == 0 and title_text:
                        cls._set_cell_shading(cell, cls.TABLE_TITLE_FILL)
                    elif row_index in {0, 1} and title_text:
                        cls._set_cell_shading(cell, cls.BPA_HEADER_FILL)
                    elif row_index == 0:
                        cls._set_cell_shading(cell, cls.BPA_HEADER_FILL)
                    else:
                        cls._set_cell_shading(cell, cls.BPA_BODY_FILL)
                elif table_key == "fdt":
                    if row_index == 0 and title_text:
                        cls._set_cell_shading(cell, cls.TABLE_TITLE_FILL)
                    elif row_index in {0, 1}:
                        cls._set_cell_shading(cell, cls.FDT_HEADER_FILL)
                    elif cell == row.cells[0]:
                        cls._set_cell_shading(cell, cls.FDT_HEADER_FILL)
                    else:
                        cls._set_cell_shading(cell, cls.FDT_BODY_FILL)
                elif table_key in {"etdah", "scared", "srs2"}:
                    if row_index == 0 and title_text:
                        cls._set_cell_shading(cell, cls.TABLE_TITLE_FILL)
                    elif row_index in {0, 1} and title_text:
                        cls._set_cell_shading(cell, cls.FDT_HEADER_FILL)
                    elif row_index == 0:
                        cls._set_cell_shading(cell, cls.FDT_HEADER_FILL)
                    elif cell == row.cells[0]:
                        cls._set_cell_shading(cell, cls.FDT_HEADER_FILL)
                    else:
                        cls._set_cell_shading(cell, cls.FDT_BODY_FILL)
                elif row_index == 0:
                    cls._set_cell_shading(cell, cls.HEADER_FILL)
                if table_key == "wisc" and row_index == 0:
                    cls._set_cell_no_wrap(cell, True)
                if table_key == "bpa" and row_index in ({0, 1} if title_text else {0}):
                    cls._set_cell_no_wrap(cell, True)
                if table_key == "fdt" and row_index in {0, 1}:
                    cls._set_cell_no_wrap(cell, True)
                if table_key in {"etdah", "scared", "srs2"} and row_index in ({0, 1} if title_text else {0}):
                    cls._set_cell_no_wrap(cell, True)
                if table_key == "etdah" and cell_index == 0:
                    cls._set_cell_no_wrap(cell, True)
                if table_key == "srs2" and cell_index == len(row.cells) - 1:
                    cls._set_cell_no_wrap(cell, True)
                for paragraph in cell.paragraphs:
                    if table_key == "wisc":
                        if row_index == 0:
                            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        elif cell_index in {0, len(row.cells) - 1}:
                            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                        else:
                            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        paragraph.paragraph_format.space_before = Pt(0)
                        paragraph.paragraph_format.space_after = Pt(0)
                        paragraph.paragraph_format.line_spacing = 1.5
                        paragraph.paragraph_format.first_line_indent = Pt(0)
                    elif table_key == "bpa":
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER if row_index == 0 and title_text else WD_ALIGN_PARAGRAPH.LEFT if cell_index == 0 else WD_ALIGN_PARAGRAPH.CENTER
                        paragraph.paragraph_format.space_before = Pt(0)
                        paragraph.paragraph_format.space_after = Pt(0)
                        paragraph.paragraph_format.line_spacing = 1.5
                        paragraph.paragraph_format.first_line_indent = Pt(0)
                    elif table_key == "fdt":
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER if row_index == 0 else WD_ALIGN_PARAGRAPH.LEFT if cell_index == 0 else WD_ALIGN_PARAGRAPH.CENTER
                        paragraph.paragraph_format.space_before = Pt(0)
                        paragraph.paragraph_format.space_after = Pt(0)
                        paragraph.paragraph_format.line_spacing = 1.5
                        paragraph.paragraph_format.first_line_indent = Pt(0)
                    elif table_key in {"etdah", "scared", "srs2"}:
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER if row_index == 0 else WD_ALIGN_PARAGRAPH.LEFT if cell_index == 0 else WD_ALIGN_PARAGRAPH.CENTER
                        paragraph.paragraph_format.space_before = Pt(0)
                        paragraph.paragraph_format.space_after = Pt(0)
                        paragraph.paragraph_format.line_spacing = 1.5
                        paragraph.paragraph_format.first_line_indent = Pt(0)
                    else:
                        paragraph.alignment = (
                            WD_ALIGN_PARAGRAPH.CENTER
                            if row_index == 0
                            else WD_ALIGN_PARAGRAPH.LEFT
                        )
                        paragraph.paragraph_format.space_after = Pt(0)
                        paragraph.paragraph_format.line_spacing = 1.5
                    paragraph.paragraph_format.space_after = Pt(0)
                    for run in paragraph.runs:
                        run.font.name = cls.FONT_NAME
                        if table_key == "wisc":
                            run.font.size = Pt(9)
                        elif table_key == "bpa":
                            run.font.size = Pt(9)
                        elif table_key == "fdt":
                            run.font.size = Pt(10) if row_index == 0 else Pt(9)
                        elif table_key in {"etdah", "scared", "srs2"}:
                            run.font.size = Pt(10) if row_index == 0 else Pt(9)
                        else:
                            run.font.size = cls.TABLE_SIZE
                        if row_index == 0 or (table_key == "fdt" and row_index == 1):
                            run.bold = True
                        if row_index == 0:
                            run.bold = False
                        if row_index == 0 and title_text:
                            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                        if table_key == "fdt" and row_index in {0, 1}:
                            run.bold = False
                        if table_key in {"wisc", "bpa"} and row_index > 0 and cell == row.cells[0]:
                            run.font.color.rgb = RGBColor(0, 0, 0)
                        if table_key == "fdt":
                            run.font.color.rgb = RGBColor(0, 0, 0)
                        if table_key in {"etdah", "scared", "srs2"}:
                            run.font.color.rgb = RGBColor(0, 0, 0)
                        if table_key == "srs2" and row_index == len(table.rows) - 1:
                            run.bold = True
                        if table_key == "srs2" and row_index == len(table.rows) - 1:
                            run.bold = True
                cell.vertical_alignment = (
                    WD_CELL_VERTICAL_ALIGNMENT.CENTER if table_key in {"wisc", "bpa", "fdt", "etdah", "scared", "srs2"} else None
                )

            if table_key == "wisc" and row_index > 0 and row.cells[0].text == "Fala Espontânea":
                merged_text = row.cells[1].text.strip()
                merged = row.cells[1]
                for idx in range(2, len(row.cells)):
                    merged = merged.merge(row.cells[idx])
                merged.text = merged_text
                row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
                for paragraph in row.cells[1].paragraphs:
                    paragraph.paragraph_format.space_before = Pt(0)
                    paragraph.paragraph_format.space_after = Pt(0)
                    paragraph.paragraph_format.line_spacing = 1.5
                    paragraph.paragraph_format.first_line_indent = Pt(0)
                    for run in paragraph.runs:
                        run.font.name = cls.FONT_NAME
                        run.font.size = Pt(9)
                row.cells[1].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

            if title_text and row_index == 0:
                cls._merge_title_row(row)
                for paragraph in row.cells[0].paragraphs:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    paragraph.paragraph_format.space_before = Pt(0)
                    paragraph.paragraph_format.space_after = Pt(0)
                    paragraph.paragraph_format.line_spacing = 1.5
                    paragraph.paragraph_format.first_line_indent = Pt(0)
                    for run in paragraph.runs:
                        run.font.name = cls.FONT_NAME
                        run.font.size = Pt(10)
                        run.bold = False
                        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                row.cells[0].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

    @classmethod
    def _format_ravlt_table(cls, table):
        table.style = None
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        cls._set_table_layout_fixed(table)
        cls._clear_table_width(table)
        cls._set_table_cell_margins(table, top=20, start=40, bottom=20, end=40)
        cls._set_table_borders(table, color="000000", size=6)

        widths = cls._table_widths("ravlt") or []
        title_text = cls._table_title_text("ravlt")
        if widths:
            cls._set_table_grid_widths(table, widths)

        for row_index, row in enumerate(table.rows):
            if row_index == 0:
                cls._set_repeat_table_header(row)
            for cell_index, cell in enumerate(row.cells):
                if row_index == 0 and title_text:
                    cls._set_cell_shading(cell, cls.TABLE_TITLE_FILL)
                elif row_index in {0, 1} and title_text:
                    cls._set_cell_shading(cell, cls.RAVLT_HEADER_FILL)
                elif row_index == 0:
                    cls._set_cell_shading(cell, cls.RAVLT_HEADER_FILL)
                if widths and cell_index < len(widths):
                    cell.width = widths[cell_index]
                cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                cls._set_cell_no_wrap(cell, True)

                for paragraph in cell.paragraphs:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER if row_index == 0 else WD_ALIGN_PARAGRAPH.LEFT if cell_index == 0 else WD_ALIGN_PARAGRAPH.CENTER

                    paragraph.paragraph_format.space_before = Pt(0)
                    paragraph.paragraph_format.space_after = Pt(0)
                    paragraph.paragraph_format.line_spacing = 1.5
                    paragraph.paragraph_format.first_line_indent = Pt(0)
                    paragraph.paragraph_format.left_indent = Pt(0)
                    paragraph.paragraph_format.right_indent = Pt(0)
                    for run in paragraph.runs:
                        run.font.name = cls.FONT_NAME
                        # Use font size 10 for RAVLT table to match requested layout
                        run.font.size = Pt(10)
                        run.bold = row_index > 0 and cell_index == 0
                        if row_index == 0 and title_text:
                            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

            if title_text and row_index == 0:
                cls._merge_title_row(row)
                for paragraph in row.cells[0].paragraphs:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    paragraph.paragraph_format.space_before = Pt(0)
                    paragraph.paragraph_format.space_after = Pt(0)
                    paragraph.paragraph_format.line_spacing = 1.5
                    paragraph.paragraph_format.first_line_indent = Pt(0)
                    for run in paragraph.runs:
                        run.font.name = cls.FONT_NAME
                        run.font.size = Pt(10)
                        run.bold = False
                        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    @classmethod
    def _apply_table_widths(cls, table, table_key: str):
        widths = cls._table_widths(table_key)
        if not widths:
            return
        cls._set_table_grid_widths(table, widths)
        for row in table.rows:
            for idx, cell in enumerate(row.cells[: len(widths)]):
                cell.width = widths[idx]

    @classmethod
    def _set_table_grid_widths(cls, table, widths):
        tbl_grid = table._tbl.tblGrid
        if tbl_grid is None:
            tbl_grid = OxmlElement("w:tblGrid")
            table._tbl.insert(1, tbl_grid)
        for child in list(tbl_grid):
            tbl_grid.remove(child)
        for width in widths:
            grid_col = OxmlElement("w:gridCol")
            grid_col.set(qn("w:w"), str(int(width.twips)))
            tbl_grid.append(grid_col)

    @classmethod
    def _table_widths(cls, table_key: str):
        return {
            "wisc": [
                Inches(1.75),
                Inches(0.95),
                Inches(0.95),
                Inches(0.95),
                Inches(0.90),
                Inches(1.15),
            ],
            "bpa": [Inches(2.35), Inches(1.15), Inches(1.00), Inches(2.00)],
            "ravlt": [
                # Desempenho: 3.11 cm
                Inches(3.11 / 2.54),
                # A1..A5: 0.93 cm each
                Inches(0.93 / 2.54), Inches(0.93 / 2.54), Inches(0.93 / 2.54), Inches(0.93 / 2.54),
                Inches(0.93 / 2.54),
                # B1: 0.93 cm
                Inches(0.93 / 2.54),
                # A6..A7: 0.93 cm each
                Inches(0.93 / 2.54),
                Inches(0.93 / 2.54),
                # R: 0.82 cm
                Inches(0.82 / 2.54),
                # ALT: 1.36 cm
                Inches(1.36 / 2.54),
                # RET: 1.36 cm
                Inches(1.36 / 2.54),
                # I.P.: 1.2 cm
                Inches(1.2 / 2.54),
                # I.R.: 1.2 cm
                Inches(1.2 / 2.54),
            ],
            "fdt": [
                Inches(1295 / 1440),
                Inches(1377 / 1440),
                Inches(1411 / 1440),
                Inches(673 / 1440),
                Inches(1284 / 1440),
                Inches(3304 / 1440),
            ],
            "etdah": [Inches(3.3), Inches(1.15), Inches(0.65), Inches(0.8), Inches(1.25)],
            "scared": [Inches(2.3), Inches(0.9), Inches(0.9), Inches(1.1), Inches(1.1)],
            "epq": [Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.8)],
            "srs2": [Inches(2.2), Inches(1.05), Inches(0.7), Inches(0.75), Inches(1.95)],
            "scale_summary": [Inches(2.2), Inches(3.0)],
        }.get(table_key)

    @classmethod
    def _set_table_layout_autofit(cls, table):
        tbl_pr = table._tbl.tblPr
        tbl_layout = tbl_pr.find(qn("w:tblLayout"))
        if tbl_layout is None:
            tbl_layout = OxmlElement("w:tblLayout")
            tbl_pr.append(tbl_layout)
        tbl_layout.set(qn("w:type"), "autofit")

    @classmethod
    def _set_table_layout_fixed(cls, table):
        tbl_pr = table._tbl.tblPr
        tbl_layout = tbl_pr.find(qn("w:tblLayout"))
        if tbl_layout is None:
            tbl_layout = OxmlElement("w:tblLayout")
            tbl_pr.append(tbl_layout)
        tbl_layout.set(qn("w:type"), "fixed")

    @classmethod
    def _set_table_width_pct(cls, table, width_pct: int):
        tbl_pr = table._tbl.tblPr
        tbl_w = tbl_pr.find(qn("w:tblW"))
        if tbl_w is None:
            tbl_w = OxmlElement("w:tblW")
            tbl_pr.append(tbl_w)
        tbl_w.set(qn("w:type"), "pct")
        tbl_w.set(qn("w:w"), str(width_pct))

    @classmethod
    def _clear_table_width(cls, table):
        tbl_pr = table._tbl.tblPr
        tbl_w = tbl_pr.find(qn("w:tblW"))
        if tbl_w is None:
            tbl_w = OxmlElement("w:tblW")
            tbl_pr.append(tbl_w)
        tbl_w.set(qn("w:type"), "auto")
        tbl_w.set(qn("w:w"), "0")

    @classmethod
    def _set_table_cell_margins(
        cls, table, top: int = 0, start: int = 0, bottom: int = 0, end: int = 0
    ):
        tbl_pr = table._tbl.tblPr
        tbl_cell_mar = tbl_pr.find(qn("w:tblCellMar"))
        if tbl_cell_mar is None:
            tbl_cell_mar = OxmlElement("w:tblCellMar")
            tbl_pr.append(tbl_cell_mar)
        for tag, value in {
            "w:top": top,
            "w:start": start,
            "w:bottom": bottom,
            "w:end": end,
        }.items():
            element = tbl_cell_mar.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tbl_cell_mar.append(element)
            element.set(qn("w:w"), str(value))
            element.set(qn("w:type"), "dxa")

    @classmethod
    def _set_table_borders(cls, table, color: str = "000000", size: int = 4):
        tbl_pr = table._tbl.tblPr
        tbl_borders = tbl_pr.find(qn("w:tblBorders"))
        if tbl_borders is None:
            tbl_borders = OxmlElement("w:tblBorders")
            tbl_pr.append(tbl_borders)
        for tag in ("w:top", "w:left", "w:bottom", "w:right", "w:insideH", "w:insideV"):
            element = tbl_borders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tbl_borders.append(element)
            element.set(qn("w:val"), "single")
            element.set(qn("w:sz"), str(size))
            element.set(qn("w:color"), color)
            element.set(qn("w:space"), "0")

    @classmethod
    def _set_cell_width_auto(cls, cell):
        tc_pr = cell._tc.get_or_add_tcPr()
        tc_w = tc_pr.find(qn("w:tcW"))
        if tc_w is None:
            tc_w = OxmlElement("w:tcW")
            tc_pr.append(tc_w)
        tc_w.set(qn("w:type"), "auto")
        tc_w.set(qn("w:w"), "0")

    @classmethod
    def _set_cell_no_wrap(cls, cell, enabled: bool):
        tc_pr = cell._tc.get_or_add_tcPr()
        no_wrap = tc_pr.find(qn("w:noWrap"))
        if enabled and no_wrap is None:
            tc_pr.append(OxmlElement("w:noWrap"))
        if not enabled and no_wrap is not None:
            tc_pr.remove(no_wrap)

    @classmethod
    def _table_cell_alignment(
        cls, table_key: str, row_index: int, cell_index: int, is_wisc_observation_row: bool = False
    ):
        if row_index == 0:
            return WD_ALIGN_PARAGRAPH.CENTER
        if is_wisc_observation_row:
            return WD_ALIGN_PARAGRAPH.LEFT
        return WD_ALIGN_PARAGRAPH.LEFT if cell_index == 0 else WD_ALIGN_PARAGRAPH.CENTER

    @classmethod
    def _merge_wisc_observation_row(cls, row):
        merged_text = row.cells[1].text.strip()
        merged = row.cells[1]
        for idx in range(2, len(row.cells)):
            merged = merged.merge(row.cells[idx])
        merged.text = merged_text

    @classmethod
    def _table_font_size(cls, table_key: str, row_index: int, cell_index: int):
        if row_index == 0:
            if table_key in {"ravlt", "fdt", "etdah", "scared", "srs2"}:
                return Pt(7.5)
            return cls.TABLE_HEADER_SIZE
        if table_key in {"ravlt", "fdt", "etdah", "scared", "srs2"} and cell_index > 0:
            return Pt(8.5)
        return cls.TABLE_SIZE

    @classmethod
    def _set_repeat_table_header(cls, row):
        tr_pr = row._tr.get_or_add_trPr()
        tbl_header = OxmlElement("w:tblHeader")
        tbl_header.set(qn("w:val"), "true")
        tr_pr.append(tbl_header)

    @classmethod
    def _set_cell_shading(cls, cell, fill: str):
        tc_pr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:fill"), fill)
        tc_pr.append(shd)

    @staticmethod
    def _num(value):
        if value is None:
            return "-"
        if isinstance(value, float):
            return f"{value:.2f}".rstrip("0").rstrip(".").replace(".", ",")
        return str(value).replace(".", ",")

    @staticmethod
    def _parse_iso_date(value):
        if not value:
            return None
        from datetime import date

        if isinstance(value, date):
            return value
        try:
            return date.fromisoformat(str(value)[:10])
        except ValueError:
            return None

    @classmethod
    def _wisc_ncp_table(cls, context: dict):
        birth_date = cls._parse_iso_date((context.get("patient") or {}).get("birth_date"))
        reference_date = cls._parse_iso_date((context.get("evaluation") or {}).get("start_date"))
        for test in context.get("validated_tests") or []:
            if test.get("instrument_code") == "wisc4" and test.get("applied_on"):
                reference_date = cls._parse_iso_date(test.get("applied_on"))
                break
        if not birth_date or not reference_date:
            return None
        try:
            years, months = _calcular_idade(birth_date, reference_date)
            return _carregar_tabela_ncp(years, months)
        except Exception:
            return None

    @staticmethod
    def _normalize_wisc_cell(cell: str) -> tuple[int | None, int | None]:
        raw = (cell or "").strip().replace(":", "-")
        if not raw or raw == "-":
            return (None, None)
        if "-" in raw:
            start, end = raw.split("-", 1)
            try:
                return (int(start), int(end))
            except ValueError:
                return (None, None)
        if raw.isdigit():
            if len(raw) == 2 and int(raw[1]) == int(raw[0]) + 1:
                return (int(raw[0]), int(raw[1]))
            if len(raw) == 4:
                left, right = raw[:2], raw[2:]
                if left.isdigit() and right.isdigit():
                    return (int(left), int(right))
            number = int(raw)
            return (number, number)
        return (None, None)

    @classmethod
    def _wisc_reference_scores(cls, table: list[dict] | None, code: str) -> tuple[str, str, str]:
        if not table:
            return ("-", "-", "-")

        rows_by_pp = {}
        for row in table:
            try:
                rows_by_pp[int(row.get("PP") or 0)] = row
            except ValueError:
                continue

        max_start, max_end = cls._normalize_wisc_cell((rows_by_pp.get(19) or {}).get(code, ""))
        if max_start is None:
            max_text = "-"
        else:
            max_text = str(max_start) if max_start == max_end else f"{max_start}-{max_end}"

        mid_start, _ = cls._normalize_wisc_cell((rows_by_pp.get(8) or {}).get(code, ""))
        _, mid_end = cls._normalize_wisc_cell((rows_by_pp.get(12) or {}).get(code, ""))
        if mid_start is None or mid_end is None:
            mid_text = "-"
        else:
            mid_text = str(mid_start) if mid_start == mid_end else f"{mid_start}-{mid_end}"

        min_start, _ = cls._normalize_wisc_cell((rows_by_pp.get(5) or {}).get(code, ""))
        min_text = str(min_start) if min_start is not None else "-"
        return (max_text, mid_text, min_text)

    @staticmethod
    def _extract_percentile_value(value):
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            numeric = "".join(ch for ch in value if ch.isdigit() or ch in ",.")
            if numeric:
                try:
                    return float(numeric.replace(",", "."))
                except ValueError:
                    return 0.0
        return 0.0

    @classmethod
    def _wisc_rows(cls, test: dict | None, context: dict, domain: str):
        payload = (test or {}).get("classified_payload") or {}
        ncp_table = cls._wisc_ncp_table(context)
        subtests = {item.get("codigo"): item for item in payload.get("subtestes") or []}
        domain_codes = {
            "funcoes_executivas": ["SM", "CN", "CO", "RM"],
            "linguagem": ["SM", "VC", "CO"],
            "gnosias_praxias": ["RM", "CB"],
        }
        rows = [[
            "Testes Utilizados",
            "Escore Máximo",
            "Escore Médio",
            "Escore Mínimo",
            "Escore Bruto",
            "Classificação",
        ]]
        for code in domain_codes.get(domain, []):
            item = subtests.get(code)
            if not item:
                continue
            score_max, score_mid, score_min = cls._wisc_reference_scores(
                ncp_table, code
            )
            rows.append(
                [
                    item.get("subteste") or "-",
                    score_max,
                    score_mid,
                    score_min,
                    cls._num(item.get("escore_bruto")),
                    item.get("classificacao") or "-",
                ]
            )
        if domain == "linguagem":
            rows.append(
                [
                    "Fala Espontânea",
                    "Dentro do esperado para a sua idade",
                    "",
                    "",
                    "",
                    "",
                ]
            )
        return rows if len(rows) > 1 else None

    @classmethod
    def _bpa_rows(cls, test: dict | None, context: dict | None = None):
        payload = (test or {}).get("classified_payload") or {}
        labels = {
            "ac": "Atenção Concentrada - AC",
            "ad": "Atenção Dividida - AD",
            "aa": "Atenção Alternada - AA",
            "ag": "Atenção Geral - AG",
        }
        rows = [["ATENÇÃO BPA", "Pontos", "Percentil", "Classificação"]]
        for item in payload.get("subtestes") or []:
            rows.append(
                [
                    labels.get(
                        item.get("codigo"),
                        item.get("subteste") or item.get("codigo") or "-",
                    ),
                    cls._num(item.get("total") or item.get("brutos")),
                    cls._num(item.get("percentil")),
                    item.get("classificacao") or "-",
                ]
            )
        return rows if len(rows) > 1 else None

    @staticmethod
    def _bpa_chart_bytes(test: dict | None):
        chart_data = (test or {}).get("bpa_chart_data") or {}
        return gerar_grafico_bpa_bytes(chart_data)

    @classmethod
    def _fdt_rows(cls, test: dict | None):
        payload = (test or {}).get("classified_payload") or {}
        errors = payload.get("erros") or {}
        rows = [
            [
                "Processo",
                "Tempo Médio",
                "Tempo Obtido",
                "Erros",
                "Desempenho",
                "Classificação",
            ]
        ]
        for item in payload.get("metric_results") or []:
            err = errors.get((item.get("codigo") or "").lower(), {})
            error_count = err.get("qtde_erros") if err else None
            table_result = cls._fdt_table_result(item.get("percentil_num"))
            rows.append(
                [
                    item.get("nome") or item.get("codigo") or "-",
                    cls._num(item.get("media")),
                    cls._num(item.get("valor")),
                    "" if error_count is None else cls._num(error_count),
                    cls._num(table_result["desempenho"]),
                    table_result["classificacao"],
                ]
            )
        return rows if len(rows) > 1 else None

    @classmethod
    def _fdt_table_result(cls, percentile: float | int | None) -> dict[str, str | int]:
        try:
            percentile_value = float(percentile)
        except (TypeError, ValueError):
            return {"desempenho": "-", "classificacao": "-"}

        if percentile_value <= 24:
            return {
                "desempenho": 5,
                "classificacao": "Indicativo de Déficit",
            }
        if percentile_value <= 30:
            return {
                "desempenho": 25,
                "classificacao": "Indicativo de Dificuldade Discreta",
            }
        if percentile_value > 65:
            return {
                "desempenho": 75,
                "classificacao": "Sem Indicativo de Déficit",
            }
        return {
            "desempenho": 50,
            "classificacao": "Sem Indicativo de Déficit",
        }

    @classmethod
    def _etdah_rows(cls, test: dict | None):
        payload = (test or {}).get("classified_payload") or {}
        results = payload.get("results") or {}
        rows = [["Escala", "Pontos Brutos", "Média", "Percentil", "Classificação"]]
        for item in results.values():
            rows.append(
                [
                    item.get("name") or "-",
                    cls._num(item.get("raw_score")),
                    cls._num(item.get("mean")),
                    cls._num(item.get("percentile_text") or item.get("percentil")),
                    item.get("classification") or item.get("classificacao") or "-",
                ]
            )
        return rows if len(rows) > 1 else None

    @classmethod
    def _ebadep_rows(cls, test: dict | None):
        payload = (test or {}).get("classified_payload") or {}
        result = payload.get("result") or payload
        if not result:
            return None
        return [
            ["Indicador", "Valor"],
            [
                "Escore Total",
                cls._num(result.get("escore_total") or result.get("pontuacao_total")),
            ],
            [
                "Percentil",
                cls._num(
                    result.get("percentil")
                    or ((result.get("normas") or {}).get("percentil"))
                ),
            ],
            ["Classificação", result.get("classificacao") or "-"],
        ]

    @classmethod
    def _scared_rows(cls, test: dict | None):
        payload = (test or {}).get("classified_payload") or {}
        rows = [["Fator", "Bruto", "Percentil", "Corte", "Classificação"]]
        for item in payload.get("analise_geral") or []:
            rows.append(
                [
                    str(item.get("fator", "")).replace("_", " ").title(),
                    cls._num(item.get("escore_bruto")),
                    cls._num(item.get("percentil") or item.get("percentual")),
                    cls._num(item.get("nota_corte")),
                    item.get("classificacao") or "-",
                ]
            )
        return rows if len(rows) > 1 else None

    @classmethod
    def _epq_rows(cls, test: dict | None):
        payload = (test or {}).get("classified_payload") or {}
        factors = payload.get("fatores") or {}
        rows = [["Fator", "Escore", "Percentil", "Classificação"]]
        for key in ("P", "E", "N", "S"):
            item = factors.get(key)
            if not item:
                continue
            rows.append(
                [
                    key,
                    cls._num(item.get("escore")),
                    cls._num(item.get("percentil")),
                    item.get("classificacao") or "-",
                ]
            )
        return rows if len(rows) > 1 else None

    @classmethod
    def _srs2_rows(cls, test: dict | None):
        payload = (test or {}).get("classified_payload") or {}
        rows = [["Escala", "Pontos Bruto", "T-Score", "Percentil", "Classificação"]]
        for item in payload.get("resultados") or []:
            rows.append(
                [
                    item.get("nome") or "-",
                    cls._num(item.get("bruto")),
                    cls._num(item.get("tscore")),
                    cls._num(item.get("percentil")),
                    item.get("classificacao") or "-",
                ]
            )
        return rows if len(rows) > 1 else None

    @classmethod
    def _build_chart_png(
        cls,
        kind: str,
        title: str,
        labels: list[str],
        values: list[float],
        ylabel: str,
        extra: dict | None = None,
    ) -> bytes | None:
        if not labels or not values:
            return None
        extra = extra or {}
        fig, ax = plt.subplots(figsize=(8, 4.5), dpi=180)
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")
        ax.set_title(title, fontsize=11, fontweight="bold", color="#23374D")
        ax.set_ylabel(ylabel, fontsize=9)
        ax.grid(axis="y", linestyle="--", alpha=0.25)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        ax.spines["left"].set_color("#94A3B8")
        ax.spines["bottom"].set_color("#94A3B8")

        if kind == "bar":
            bars = ax.bar(
                labels, values, color="#2F6DB3", edgecolor="#1E3A5F", linewidth=0.6
            )
            for bar, value in zip(bars, values):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    cls._num(value),
                    ha="center",
                    va="bottom",
                    fontsize=8,
                )
        else:
            ax.plot(labels, values, marker="o", color="#2F6DB3", linewidth=2.2)
            if extra.get("expected"):
                ax.plot(
                    labels,
                    extra["expected"],
                    linestyle="--",
                    color="#4caf50",
                    linewidth=1.5,
                    label="Esperado",
                )
            if extra.get("minimum"):
                ax.plot(
                    labels,
                    extra["minimum"],
                    linestyle=":",
                    color="#f59e0b",
                    linewidth=1.5,
                    label="Mínimo",
                )
            if extra.get("expected") or extra.get("minimum"):
                ax.legend(fontsize=8)

        ymax = max(values + extra.get("expected", []) + extra.get("minimum", []) + [1])
        ax.set_ylim(0, ymax * 1.2)
        ax.tick_params(axis="x", labelrotation=0, labelsize=8)
        ax.tick_params(axis="y", labelsize=8)
        plt.tight_layout()

        output = BytesIO()
        fig.savefig(output, format="png", bbox_inches="tight", facecolor="white")
        plt.close(fig)
        return output.getvalue()

    @classmethod
    def _build_wisc_chart_png(
        cls, labels: list[str], values: list[float], errors: list[float] | None = None
    ) -> bytes | None:
        if not labels or not values:
            return None

        errors = errors or [0.0] * len(values)
        regular_font = None
        if cls.LOCAL_LIBERATION_SERIF.exists():
            font_manager.fontManager.addfont(str(cls.LOCAL_LIBERATION_SERIF))
            regular_font = font_manager.FontProperties(fname=str(cls.LOCAL_LIBERATION_SERIF))
        title_font = regular_font.copy() if regular_font else None
        if title_font:
            title_font.set_size(15)
        x_label_font = regular_font.copy() if regular_font else None
        if x_label_font:
            x_label_font.set_size(11)
        y_label_font = regular_font.copy() if regular_font else None
        if y_label_font:
            y_label_font.set_size(11)
        y_tick_font = regular_font.copy() if regular_font else None
        if y_tick_font:
            y_tick_font.set_size(10)
        x = list(range(len(labels)))

        fig, ax = plt.subplots(figsize=(10.2, 4.7), dpi=170)
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")
        bands = [
            (130, 160, "#b8e86f"),
            (115, 130, "#c6ef72"),
            (85, 115, "#b8c4d1"),
            (80, 85, "#fff36a"),
            (40, 80, "#fff97e"),
        ]
        for y0, y1, color in bands:
            ax.axhspan(y0, y1, facecolor=color, alpha=1.0, zorder=0)

        ax.set_ylim(40, 160)
        ax.set_xlim(-0.5, len(labels) - 0.5)
        ax.yaxis.set_major_locator(plt.MultipleLocator(10))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(5))
        ax.grid(axis="y", which="major", color="#d7e67a", linewidth=0.8, zorder=1)
        ax.grid(axis="x", color="#e8e8e8", linewidth=0.8, zorder=1)
        ax.set_axisbelow(True)

        color_by_label = {
            "ICV": "#4d78be",
            "IOP": "#f57f2a",
            "IMO": "#7f7f7f",
            "IVP": "#ffc000",
            "QI Total": "#76b043",
            "GAI": "#4d78be",
            "CPI": "#b45f06",
        }
        colors = [color_by_label.get(label, "#5B9BD5") for label in labels]

        ax.bar(
            x,
            values,
            width=0.72,
            color=colors,
            edgecolor="none",
            zorder=3,
        )

        ax.errorbar(
            x,
            values,
            yerr=errors,
            fmt="none",
            ecolor="black",
            elinewidth=1.1,
            capsize=3,
            capthick=1.1,
            zorder=4,
        )

        for xi, value in zip(x, values):
            ax.text(
                xi,
                43,
                cls._num(value),
                ha="center",
                va="bottom",
                fontsize=10,
                color="#1f3864",
                fontproperties=regular_font,
                zorder=4,
            )

        ax.set_title(
            "WISC-IV INDICES QIs",
            color="#5a8d2a",
            pad=10,
            fontproperties=title_font or regular_font,
            fontweight="normal",
        )
        ax.set_ylabel(
            "Pontos Compostos",
            color="#444444",
            fontproperties=y_label_font or regular_font,
        )
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=10, fontproperties=x_label_font or regular_font)
        ax.tick_params(axis="y", labelsize=10, colors="#444444")
        ax.tick_params(axis="x", pad=3, colors="#444444")
        if y_tick_font:
            for label in ax.get_yticklabels():
                label.set_fontproperties(y_tick_font)

        ax.spines["left"].set_color("#444444")
        ax.spines["bottom"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        output = BytesIO()
        plt.tight_layout()
        fig.savefig(output, format="png", bbox_inches="tight", facecolor="white")
        plt.close(fig)
        return output.getvalue()

    @classmethod
    def _wisc_chart(cls, test: dict | None):
        payload = cls._wisc_payload(test)
        labels, values, errors = [], [], []
        index_labels = {
            "icv": "ICV",
            "iop": "IOP",
            "imt": "IMO",
            "ivp": "IVP",
        }
        for code in ("icv", "iop", "imt", "ivp"):
            item = next(
                (entry for entry in payload.get("indices") or [] if entry.get("indice") == code),
                None,
            )
            if not item:
                continue
            labels.append(index_labels[code])
            values.append(float(item.get("escore_composto") or 0))
            interval = item.get("intervalo_confianca") or (0, 0)
            if isinstance(interval, (list, tuple)) and len(interval) == 2:
                errors.append(abs(float(interval[1]) - float(interval[0])) / 2)
            else:
                errors.append(0.0)
        qit = payload.get("qit_data") or {}
        if qit.get("escore_composto"):
            labels.append("QI Total")
            values.append(float(qit.get("escore_composto") or 0))
            interval = qit.get("intervalo_confianca") or (0, 0)
            if isinstance(interval, (list, tuple)) and len(interval) == 2:
                errors.append(abs(float(interval[1]) - float(interval[0])) / 2)
            else:
                errors.append(0.0)
        for key, label in (("gai_data", "GAI"), ("cpi_data", "CPI")):
            item = payload.get(key) or {}
            if not item.get("escore_composto"):
                continue
            labels.append(label)
            values.append(float(item.get("escore_composto") or 0))
            interval = item.get("intervalo_confianca") or (0, 0)
            if isinstance(interval, (list, tuple)) and len(interval) == 2:
                errors.append(abs(float(interval[1]) - float(interval[0])) / 2)
            else:
                errors.append(0.0)
        return cls._build_wisc_chart_png(labels, values, errors)

    @classmethod
    def _ravlt_chart(cls, test: dict | None):
        payload = (
            (test or {}).get("classified_payload")
            or (test or {}).get("computed_payload")
            or {}
        )
        labels = ["A1", "A2", "A3", "A4", "A5", "B1", "A6", "A7"]
        values = [
            float(payload.get("a1") or 0),
            float(payload.get("a2") or 0),
            float(payload.get("a3") or 0),
            float(payload.get("a4") or 0),
            float(payload.get("a5") or 0),
            float(payload.get("b1") or payload.get("b") or 0),
            float(payload.get("a6") or 0),
            float(payload.get("a7") or 0),
        ]
        expected = [6, 8, 10, 11, 12, 5, 10, 10]
        minimum = [5, 7, 8, 9, 10, 4, 8, 7]
        return cls._build_chart_png(
            "line",
            "Curva de aprendizagem no RAVLT",
            labels,
            values,
            "Pontos",
            {"expected": expected, "minimum": minimum},
        )

    @classmethod
    def _fdt_chart(cls, test: dict | None, automatic: bool):
        payload = (test or {}).get("classified_payload") or {}
        target = "Processos Automaticos" if automatic else "Processos Controlados"
        items = [
            item
            for item in payload.get("metric_results") or []
            if item.get("categoria") == target
        ]
        labels = [item.get("nome") or item.get("codigo") or "FDT" for item in items]
        values = [float(item.get("percentil_num") or 0) for item in items]
        title = (
            "FDT - Processos Automáticos"
            if automatic
            else "FDT - Processos Controlados"
        )
        return cls._build_chart_png("bar", title, labels, values, "Percentil")

    @classmethod
    def _etdah_chart(cls, test: dict | None):
        payload = (test or {}).get("classified_payload") or {}
        results = payload.get("results") or {}
        labels = []
        values = []
        for item in results.values():
            labels.append((item.get("name") or "Escala")[:12])
            values.append(
                cls._extract_percentile_value(
                    item.get("percentile_text") or item.get("percentil")
                )
            )
        return cls._build_chart_png(
            "bar", "Perfil no E-TDAH", labels, values, "Percentil"
        )

    @classmethod
    def _scared_chart(cls, test: dict | None):
        payload = (test or {}).get("classified_payload") or {}
        labels = []
        values = []
        for item in payload.get("analise_geral") or []:
            labels.append(str(item.get("fator", "")).replace("_", " ").title()[:14])
            values.append(float(item.get("percentil") or item.get("percentual") or 0))
        return cls._build_chart_png(
            "bar", "Perfil no SCARED", labels, values, "Percentil"
        )

    @classmethod
    def _epq_chart(cls, test: dict | None):
        payload = (test or {}).get("classified_payload") or {}
        factors = payload.get("fatores") or {}
        labels = []
        values = []
        for key in ("P", "E", "N", "S"):
            item = factors.get(key)
            if not item:
                continue
            labels.append(key)
            values.append(float(item.get("percentil") or 0))
        return cls._build_chart_png(
            "bar", "Perfil de personalidade no EPQ-J", labels, values, "Percentil"
        )

    @classmethod
    def _srs2_chart(cls, test: dict | None):
        payload = (test or {}).get("classified_payload") or {}
        labels = []
        values = []
        for item in payload.get("resultados") or []:
            labels.append((item.get("nome") or "Escala")[:12])
            values.append(float(item.get("tscore") or 0))
        return cls._build_chart_png(
            "bar", "Perfil social no SRS-2", labels, values, "T-Score"
        )
