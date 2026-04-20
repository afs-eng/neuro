from __future__ import annotations

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
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.shared import Inches, Pt, RGBColor
from docx.shared import Cm

from apps.reports.models import Report
from apps.reports.builders.references_builder import build_references
from apps.reports.services.report_context_service import ReportContextService
from apps.tests.wisc4.calculators import _calcular_idade, _carregar_tabela_ncp


class ReportExportService:
    DEFAULT_TEMPLATE_PATH = settings.BASE_DIR / "laudo-modelo.docx"
    ADOLESCENT_TEMPLATE_PATH = settings.BASE_DIR / "Modelo-Adolescente.docx"
    FONT_NAME = "Times New Roman"
    BODY_SIZE = Pt(12)
    TABLE_SIZE = Pt(9)
    TITLE_SIZE = Pt(12)
    CAPTION_SIZE = Pt(9)
    BODY_LINE_SPACING = 1.5
    IDENTIFICATION_LINE_SPACING = 1.15
    HEADING_SPACE_BEFORE = Pt(10)
    HEADING_SPACE_AFTER = Pt(4)
    SUBHEADING_SPACE_BEFORE = Pt(6)
    SUBHEADING_SPACE_AFTER = Pt(2)
    BODY_SPACE_AFTER = Pt(0)
    IMAGE_WIDTH = Inches(6.2)
    TABLE_WIDTH = Inches(6.2)
    ACCENT_COLOR = "2F6DB3"
    HEADER_FILL = "DCE6F1"
    WISC_HEADER_FILL = "A8D08D"
    WISC_NAME_FILL = "538135"
    WISC_VALUE_FILL = "E2EFD9"
    LOCAL_LIBERATION_SERIF = Path.home() / ".local/share/fonts/liberation/LiberationSerif-Regular.ttf"
    LOCAL_LIBERATION_SERIF_BOLD = Path.home() / ".local/share/fonts/liberation/LiberationSerif-Bold.ttf"
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
            cls._apply_base_styles(document)
            cls._replace_simple_sections(document, sections)
            cls._rebuild_qualitative_section(document, sections, context)

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
        template_path = cls.ADOLESCENT_TEMPLATE_PATH
        document = (
            Document(str(template_path)) if template_path.exists() else Document()
        )
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
        cls._append_subheading(document, "Motivo do Encaminhamento")
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
        cls._append_subheading(document, "História Pessoal")
        cls._append_paragraph(
            document,
            sections.get("historia_pessoal")
            or "Sem conteúdo disponível para esta seção.",
        )

        cls._append_heading(document, "5. EFICIÊNCIA COGNITIVA")
        cls._append_wisc_global_block(document, cls._find_test(context, "wisc4"), context)
        cls._append_chart(
            document,
            "Desempenho no WISC-IV",
            cls._wisc_chart(
                (context.get("validated_tests") or [{}])[0]
                if any(
                    t.get("instrument_code") == "wisc4"
                    for t in context.get("validated_tests") or []
                )
                else None
            ),
        )
        legend_paragraph = document.add_paragraph(cls._wisc_chart_legend())
        cls._format_chart_legend_paragraph(legend_paragraph)
        cls._append_subheading(document, "Subescalas WISC-IV")
        cls._append_subheading(document, "Funções Executivas")
        cls._append_table_with_interpretation(
            document,
            cls._wisc_rows(
                cls._find_test(context, "wisc4"), context, "funcoes_executivas"
            ),
            "wisc",
            sections.get("funcoes_executivas"),
        )
        cls._append_subheading(document, "Linguagem")
        cls._append_table_with_interpretation(
            document,
            cls._wisc_rows(cls._find_test(context, "wisc4"), context, "linguagem"),
            "wisc",
            sections.get("linguagem"),
        )
        cls._append_subheading(document, "Gnosias e Praxias")
        cls._append_table_with_interpretation(
            document,
            cls._wisc_rows(
                cls._find_test(context, "wisc4"), context, "gnosias_praxias"
            ),
            "wisc",
            sections.get("gnosias_praxias"),
        )
        cls._append_subheading(document, "Memória e Aprendizagem")
        cls._append_table_with_interpretation(
            document,
            cls._wisc_memory_rows(cls._find_test(context, "wisc4"), context),
            "wisc",
            sections.get("memoria_aprendizagem"),
        )

        cls._append_heading(
            document, "BPA-2 – BATERIA PSICOLÓGICA PARA AVALIAÇÃO DA ATENÇÃO"
        )
        cls._append_paragraph(
            document,
            "A Bateria Psicológica para Avaliação da Atenção-2 (BPA-2) mensura a capacidade geral de atenção, avaliando individualmente atenção concentrada, dividida, alternada e geral.",
        )
        cls._append_table_with_interpretation(
            document,
            cls._bpa_rows(cls._find_test(context, "bpa2")),
            "bpa",
            sections.get("bpa2") or sections.get("atencao"),
        )
        cls._append_chart(
            document,
            "Gráfico BPA-2 – Resultados da avaliação da atenção",
            cls._bpa_chart(cls._find_test(context, "bpa2")),
        )

        cls._append_heading(document, "RAVLT – REY AUDITORY VERBAL LEARNING TEST")
        cls._append_paragraph(
            document,
            "O RAVLT avalia memória verbal, capacidade de aprendizado auditivo e retenção de informações ao longo do tempo.",
        )
        cls._append_chart(
            document,
            "Gráfico RAVLT – Resultados",
            cls._ravlt_chart(cls._find_test(context, "ravlt")),
        )
        cls._append_table_with_interpretation(
            document,
            cls._ravlt_compact_rows(cls._find_test(context, "ravlt")),
            "ravlt_compact",
            sections.get("ravlt") or sections.get("memoria_aprendizagem"),
        )

        cls._append_heading(document, "FDT – TESTE DOS CINCO DÍGITOS")
        cls._append_paragraph(
            document,
            "O FDT avalia processos automáticos e controlados, incluindo velocidade de processamento, controle inibitório, alternância e flexibilidade cognitiva.",
        )
        cls._append_table_with_interpretation(
            document,
            cls._fdt_rows(cls._find_test(context, "fdt")),
            "fdt",
            sections.get("fdt") or sections.get("funcoes_executivas"),
        )
        cls._append_chart(
            document,
            "Gráfico FDT – Processos Automáticos",
            cls._fdt_chart(cls._find_test(context, "fdt"), automatic=True),
        )
        cls._append_chart(
            document,
            "Gráfico FDT – Processos Controlados",
            cls._fdt_chart(cls._find_test(context, "fdt"), automatic=False),
        )

        if cls._find_test(context, "etdah_pais"):
            cls._append_heading(document, "E-TDAH-PAIS")
            cls._append_paragraph(
                document,
                "A Escala E-TDAH-PAIS identifica manifestações comportamentais e emocionais associadas ao TDAH a partir da percepção dos responsáveis.",
            )
            cls._append_table_with_interpretation(
                document,
                cls._etdah_rows(cls._find_test(context, "etdah_pais")),
                "etdah",
                sections.get("etdah_pais")
                or sections.get("aspectos_emocionais_comportamentais"),
            )
            cls._append_chart(
                document,
                "Gráfico E-TDAH-PAIS – Resultados",
                cls._etdah_chart(cls._find_test(context, "etdah_pais")),
            )

        if cls._find_test(context, "etdah_ad"):
            cls._append_heading(document, "E-TDAH-AD")
            cls._append_paragraph(
                document,
                "O E-TDAH-AD investiga sintomas relacionados à atenção, hiperatividade, impulsividade e aspectos emocionais a partir do autorrelato do adolescente.",
            )
            cls._append_table_with_interpretation(
                document,
                cls._etdah_rows(cls._find_test(context, "etdah_ad")),
                "etdah",
                sections.get("etdah_ad")
                or sections.get("aspectos_emocionais_comportamentais"),
            )
            cls._append_chart(
                document,
                "Gráfico E-TDAH-AD – Resultados",
                cls._etdah_chart(cls._find_test(context, "etdah_ad")),
            )

        if cls._find_test(context, "scared"):
            cls._append_heading(
                document,
                "SCARED – SCREEN FOR CHILD ANXIETY RELATED EMOTIONAL DISORDERS",
            )
            cls._append_paragraph(
                document,
                "O SCARED rastreia sintomas ansiosos, incluindo pânico, ansiedade generalizada, ansiedade de separação, fobia social e evitação escolar.",
            )
            cls._append_table_with_interpretation(
                document,
                cls._scared_rows(cls._find_test(context, "scared")),
                "scared",
                sections.get("scared")
                or sections.get("aspectos_emocionais_comportamentais"),
            )
            cls._append_chart(
                document,
                "Gráfico SCARED – Resultados",
                cls._scared_chart(cls._find_test(context, "scared")),
            )

        if cls._find_test(context, "epq_j"):
            cls._append_heading(
                document, "EPQ-J – INVENTÁRIO DE PERSONALIDADE DE EYSENCK PARA JOVENS"
            )
            cls._append_table_with_interpretation(
                document,
                cls._epq_rows(cls._find_test(context, "epq_j")),
                "epq",
                sections.get("epq_j")
                or sections.get("aspectos_emocionais_comportamentais"),
            )
            cls._append_chart(
                document,
                "Gráfico EPQ-J – Resultados dos percentis",
                cls._epq_chart(cls._find_test(context, "epq_j")),
            )

        if cls._find_test(context, "srs2"):
            cls._append_heading(document, "SRS-2 – ESCALA DE RESPONSIVIDADE SOCIAL")
            cls._append_paragraph(
                document,
                "A SRS-2 avalia aspectos da interação social e comportamentos associados ao espectro autista, exigindo sempre integração clínica cuidadosa.",
            )
            cls._append_table_with_interpretation(
                document,
                cls._srs2_rows(cls._find_test(context, "srs2")),
                "srs2",
                sections.get("srs2")
                or sections.get("aspectos_emocionais_comportamentais"),
            )
            cls._append_chart(
                document,
                "Gráfico SRS-2 – Resultados",
                cls._srs2_chart(cls._find_test(context, "srs2")),
            )

        cls._append_heading(document, "CONCLUSÃO")
        cls._append_paragraph(
            document,
            sections.get("conclusao") or "Sem conteúdo disponível para esta seção.",
        )
        cls._append_subheading(document, "Sugestões de Conduta (Encaminhamentos):")
        for bullet in cls._split_bullets(sections.get("sugestoes_conduta") or ""):
            cls._append_bullet(document, bullet)

        cls._append_heading(document, "A EQUIPE MULTIDISCIPLINAR")
        for paragraph in cls._institutional_paragraphs(report):
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

        cls._append_heading(document, "REFERÊNCIAS BIBLIOGRÁFICAS")
        for ref in cls._references_list(context):
            cls._append_paragraph(document, ref)
        return document

    @classmethod
    def _apply_base_styles(cls, document: Document):
        for style_name in ("Normal",):
            style = document.styles[style_name]
            style.font.name = cls.FONT_NAME
            style.font.size = cls.BODY_SIZE
            style.paragraph_format.space_before = Pt(0)
            style.paragraph_format.space_after = Pt(0)
            style.paragraph_format.line_spacing = cls.BODY_LINE_SPACING

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
            anchor = cls._insert_paragraph_after(anchor, line)
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
            anchor = cls._insert_paragraph_after(anchor, text)
            cls._format_subtitle_paragraph(anchor)

        def add_text(text: str):
            nonlocal anchor
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
                    anchor = cls._insert_paragraph_after(anchor, line)
                    if line.startswith("Capacidade Cognitiva Global:"):
                        cls._append_wisc_intro_paragraph(anchor, line)
                    else:
                        cls._format_left_body_paragraph(anchor)

        def add_table(caption: str, rows: list[list[str]] | None, table_key: str):
            nonlocal anchor, table_index
            if not rows:
                return
            anchor = cls._insert_paragraph_after(
                anchor, f"Tabela {table_index}. {caption}"
            )
            cls._format_caption_paragraph(anchor)
            table = cls._insert_table_after(anchor, rows)
            cls._format_table(table, table_key)
            anchor = cls._insert_paragraph_after_table(table, "")
            table_index += 1

        def add_chart(caption: str, image_bytes: bytes | None):
            nonlocal anchor, chart_index
            if not image_bytes:
                return
            anchor = cls._insert_paragraph_after(
                anchor, f"Gráfico {chart_index}. {caption}"
            )
            cls._format_caption_paragraph(anchor)
            anchor = cls._insert_paragraph_after(anchor, "")
            run = anchor.runs[0] if anchor.runs else anchor.add_run()
            run.add_picture(BytesIO(image_bytes), width=cls.IMAGE_WIDTH)
            anchor.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if caption == "Índices do WISC-IV":
                anchor = cls._insert_paragraph_after(anchor, cls._wisc_chart_legend())
                cls._format_chart_legend_paragraph(anchor)
            chart_index += 1

        anchor = cls._insert_wisc_global_block_after(anchor, tests.get("wisc4"), context)
        add_chart("Índices do WISC-IV", cls._wisc_chart(tests.get("wisc4")))

        if is_adolescent:
            add_title("Funções Executivas")
            add_text(sections.get("funcoes_executivas", ""))
            add_table(
                "Resultados das Funções Executivas",
                cls._wisc_rows(tests.get("wisc4"), context, "funcoes_executivas"),
                "wisc",
            )

            add_title("Linguagem")
            add_text(sections.get("linguagem", ""))
            add_table(
                "Resultados da Linguagem",
                cls._wisc_rows(tests.get("wisc4"), context, "linguagem"),
                "wisc",
            )

            add_title("Gnosias e Praxias")
            add_text(sections.get("gnosias_praxias", ""))
            add_table(
                "Resultados de Gnosias e Praxias",
                cls._wisc_rows(tests.get("wisc4"), context, "gnosias_praxias"),
                "wisc",
            )

            add_title("Memória e Aprendizagem")
            add_text(sections.get("memoria_aprendizagem", ""))
            add_table(
                "Resultados da Memória e Aprendizagem",
                cls._wisc_memory_rows(tests.get("wisc4"), context),
                "wisc",
            )

            add_title("BPA-2 Bateria Psicológica para Avaliação da Atenção")
            add_text(sections.get("atencao", ""))
            add_table("Resultados da BPA-2", cls._bpa_rows(tests.get("bpa2")), "bpa")
            add_chart("Perfil atencional no BPA-2", cls._bpa_chart(tests.get("bpa2")))

            add_title("RAVLT Rey Auditory Verbal Learning Test")
            add_text(sections.get("ravlt", sections.get("memoria_aprendizagem", "")))
            add_chart(
                "Curva de aprendizagem no RAVLT", cls._ravlt_chart(tests.get("ravlt"))
            )
            add_table(
                "Resultados do RAVLT", cls._ravlt_rows(tests.get("ravlt")), "ravlt"
            )

            add_title("FDT - Teste dos Cinco Dígitos")
            add_text(sections.get("fdt", sections.get("funcoes_executivas", "")))
            add_table("Resultados do FDT", cls._fdt_rows(tests.get("fdt")), "fdt")
            add_chart(
                "FDT - Processos Automáticos",
                cls._fdt_chart(tests.get("fdt"), automatic=True),
            )
            add_chart(
                "FDT - Processos Controlados",
                cls._fdt_chart(tests.get("fdt"), automatic=False),
            )

            add_title("E-TDAH-PAIS")
            add_text(
                sections.get(
                    "etdah_pais",
                    sections.get("aspectos_emocionais_comportamentais", ""),
                )
            )
            add_table(
                "Resultados do E-TDAH-PAIS",
                cls._etdah_rows(tests.get("etdah_pais")),
                "etdah",
            )
            add_chart(
                "Perfil no E-TDAH-PAIS",
                cls._etdah_chart(tests.get("etdah_pais")),
            )

            add_title("E-TDAH-AD")
            add_text(
                sections.get(
                    "etdah_ad", sections.get("aspectos_emocionais_comportamentais", "")
                )
            )
            add_table(
                "Resultados do E-TDAH-AD",
                cls._etdah_rows(tests.get("etdah_ad")),
                "etdah",
            )
            add_chart("Perfil no E-TDAH-AD", cls._etdah_chart(tests.get("etdah_ad")))

            add_title("SCARED")
            add_text(
                sections.get(
                    "scared", sections.get("aspectos_emocionais_comportamentais", "")
                )
            )
            add_table(
                "Resultados do SCARED", cls._scared_rows(tests.get("scared")), "scared"
            )
            add_chart("Perfil no SCARED", cls._scared_chart(tests.get("scared")))

            add_title("EPQ-J")
            add_text(
                sections.get(
                    "epq_j", sections.get("aspectos_emocionais_comportamentais", "")
                )
            )
            add_table("Resultados do EPQ-J", cls._epq_rows(tests.get("epq_j")), "epq")
            add_chart(
                "Perfil de personalidade no EPQ-J", cls._epq_chart(tests.get("epq_j"))
            )

            add_title("SRS-2 Escala de Responsividade Social")
            add_text(
                sections.get(
                    "srs2", sections.get("aspectos_emocionais_comportamentais", "")
                )
            )
            add_table("Resultados do SRS-2", cls._srs2_rows(tests.get("srs2")), "srs2")
            add_chart("Perfil social no SRS-2", cls._srs2_chart(tests.get("srs2")))

            add_title("Conclusão e Hipótese Diagnóstica")
            add_text(
                sections.get("hipotese_diagnostica", sections.get("conclusao", ""))
            )
        else:
            add_title("Atenção")
            add_text(sections.get("atencao", ""))
            add_table("Resultados da BPA-2", cls._bpa_rows(tests.get("bpa2")), "bpa")
            add_chart("Perfil atencional no BPA-2", cls._bpa_chart(tests.get("bpa2")))

            add_title("Memória e Aprendizagem")
            add_text(sections.get("memoria_aprendizagem", ""))
            add_table(
                "Resultados do RAVLT", cls._ravlt_rows(tests.get("ravlt")), "ravlt"
            )
            add_chart(
                "Curva de aprendizagem no RAVLT", cls._ravlt_chart(tests.get("ravlt"))
            )

            add_title("Funções Executivas")
            add_text(sections.get("funcoes_executivas", ""))
            add_table("Resultados do FDT", cls._fdt_rows(tests.get("fdt")), "fdt")
            add_chart(
                "FDT - Processos Automáticos",
                cls._fdt_chart(tests.get("fdt"), automatic=True),
            )
            add_chart(
                "FDT - Processos Controlados",
                cls._fdt_chart(tests.get("fdt"), automatic=False),
            )

            add_title("Aspectos Emocionais, Comportamentais e Escalas Complementares")
            add_text(sections.get("aspectos_emocionais_comportamentais", ""))
            add_table(
                "Resultados do E-TDAH",
                cls._etdah_rows(tests.get("etdah_ad") or tests.get("etdah_pais")),
                "etdah",
            )
            add_chart(
                "Perfil no E-TDAH",
                cls._etdah_chart(tests.get("etdah_ad") or tests.get("etdah_pais")),
            )
            add_table(
                "Resultados do SCARED", cls._scared_rows(tests.get("scared")), "scared"
            )
            add_chart("Perfil no SCARED", cls._scared_chart(tests.get("scared")))
            add_table("Resultados do EPQ-J", cls._epq_rows(tests.get("epq_j")), "epq")
            add_chart(
                "Perfil de personalidade no EPQ-J", cls._epq_chart(tests.get("epq_j"))
            )
            add_table("Resultados do SRS-2", cls._srs2_rows(tests.get("srs2")), "srs2")
            add_chart("Perfil social no SRS-2", cls._srs2_chart(tests.get("srs2")))
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
    def _insert_table_after(cls, paragraph, rows: list[list[str]]):
        parent = paragraph._parent
        table = parent.add_table(rows=0, cols=len(rows[0]))
        tbl = table._tbl
        tbl.getparent().remove(tbl)
        paragraph._p.addnext(tbl)
        for row_values in rows:
            row = table.add_row().cells
            for index, value in enumerate(row_values):
                row[index].text = value
        return Table(tbl, parent)

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
        paragraph.paragraph_format.first_line_indent = Cm(1.25)
        for run in paragraph.runs:
            run.font.name = cls.FONT_NAME
            run.font.size = cls.BODY_SIZE

    @classmethod
    def _format_left_body_paragraph(cls, paragraph):
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = cls.BODY_SPACE_AFTER
        paragraph.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
        paragraph.paragraph_format.first_line_indent = Pt(0)
        for run in paragraph.runs:
            run.font.name = cls.FONT_NAME
            run.font.size = cls.BODY_SIZE

    @classmethod
    def _append_wisc_intro_paragraph(cls, paragraph, text: str):
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = cls.BODY_SPACE_AFTER
        paragraph.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
        paragraph.paragraph_format.first_line_indent = Cm(1.25)

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
    def _insert_wisc_global_block_after(cls, anchor, test: dict | None, context: dict):
        intro = cls._wisc_global_intro_text(test, context)
        anchor = cls._insert_paragraph_after(anchor, "")
        cls._append_wisc_intro_paragraph(anchor, intro)
        for lead, tail in cls._wisc_global_bullet_parts(test):
            anchor = cls._insert_paragraph_after(anchor, "")
            cls._append_wisc_global_bullet(anchor, lead, tail)
        return anchor

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
        if not text:
            return
        p = document.add_paragraph()
        p.alignment = (
            WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.JUSTIFY
        )
        r = p.add_run(text)
        r.font.name = cls.FONT_NAME
        r.font.size = cls.BODY_SIZE
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = cls.BODY_SPACE_AFTER
        p.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
        p.paragraph_format.first_line_indent = Pt(0 if center else Cm(1.25))

    @classmethod
    def _append_identification_text(cls, document, text: str):
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
        p = document.add_paragraph()
        a = p.add_run(f"{label}: ")
        a.font.name = cls.FONT_NAME
        a.font.size = cls.BODY_SIZE
        a.bold = True
        b = p.add_run(str(value or "Não informado"))
        b.font.name = cls.FONT_NAME
        b.font.size = cls.BODY_SIZE
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = cls.IDENTIFICATION_LINE_SPACING
        p.paragraph_format.first_line_indent = Pt(0)

    @classmethod
    def _append_bullet(cls, document, text: str):
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
    def _append_table_with_interpretation(
        cls,
        document,
        rows,
        table_key: str,
        interpretation: str | None,
        caption: str | None = None,
    ):
        if rows:
            if caption:
                caption_paragraph = document.add_paragraph()
                caption_run = caption_paragraph.add_run(caption)
                caption_run.font.name = cls.FONT_NAME
                caption_run.font.size = Pt(10)
                caption_run.italic = True
            table = document.add_table(rows=0, cols=len(rows[0]))
            for row_values in rows:
                row = table.add_row().cells
                for idx, value in enumerate(row_values):
                    row[idx].text = str(value)
            cls._format_table(table, table_key)
        if interpretation:
            cls._append_paragraph(document, f"Interpretação: {interpretation}")

    @classmethod
    def _append_chart(cls, document, caption: str, image_bytes: bytes | None):
        if not image_bytes:
            return
        p = document.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(caption)
        r.font.name = cls.FONT_NAME
        r.font.size = Pt(10)
        r.italic = True
        img = document.add_paragraph()
        img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img.add_run().add_picture(BytesIO(image_bytes), width=cls.IMAGE_WIDTH)

    @classmethod
    def _format_chart_legend_paragraph(cls, paragraph):
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.paragraph_format.line_spacing = cls.BODY_LINE_SPACING
        paragraph.paragraph_format.first_line_indent = Pt(0)
        for run in paragraph.runs:
            run.font.name = cls.FONT_NAME
            run.font.size = Pt(9)
            run.italic = True

    @classmethod
    def _wisc_chart_legend(cls) -> str:
        return (
            "Gráfico 1 WISC-IV - INDICES DE QIS: Índice de Compreensão Verbal (ICV): composto por provas que avaliam as habilidades verbais por meio do raciocínio, compreensão e conceituação. "
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
    def _institutional_paragraphs(cls, report):
        email = getattr(getattr(report, "author", None), "email", "") or ""
        return [
            "A Avaliação Neuropsicológica, quando bem fundamentada, é essencial para direcionar a reabilitação cognitiva e fornecer subsídios para outros profissionais em suas respectivas áreas de atuação.",
            "É importante que o documento seja lido na íntegra, e não apenas a conclusão, para que se compreenda plenamente o raciocínio clínico utilizado ao longo de todo o processo avaliativo.",
            f"Com a devida autorização por escrito dos responsáveis, coloco-me à disposição para esclarecimentos e discussões sobre o exame{f', podendo ser contatada pelo e-mail {email}' if email else ''}.",
            "Importante ressaltar que este documento não deve ser utilizado para fins diferentes daqueles especificados no item de identificação do documento e possui caráter sigiloso.",
            "Ressalta-se que o ser humano possui uma natureza dinâmica; não definitiva e não cristalizada. Os resultados aqui expostos dizem respeito ao funcionamento atual do paciente e podem sofrer alterações posteriores.",
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
    def _ravlt_compact_rows(cls, test: dict | None):
        payload = (
            (test or {}).get("classified_payload")
            or (test or {}).get("computed_payload")
            or {}
        )
        headers = [
            "Desempenho",
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
        row = [
            "Obtido",
            cls._num(payload.get("a1")),
            cls._num(payload.get("a2")),
            cls._num(payload.get("a3")),
            cls._num(payload.get("a4")),
            cls._num(payload.get("a5")),
            cls._num(payload.get("b1") or payload.get("b")),
            cls._num(payload.get("a6")),
            cls._num(payload.get("a7")),
            cls._num(payload.get("r")),
            cls._num(payload.get("alt")),
            cls._num(payload.get("ret")),
            cls._num(payload.get("ip")),
            cls._num(payload.get("ir")),
        ]
        return [headers, row] if any(value != "-" for value in row[1:]) else None

    @classmethod
    def _format_table(cls, table, table_key: str):
        table.style = "Table Grid"
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        cls._apply_table_widths(table, table_key)
        for row_index, row in enumerate(table.rows):
            if row_index == 0:
                cls._set_repeat_table_header(row)
            for cell in row.cells:
                if table_key == "wisc":
                    if row_index == 0:
                        cls._set_cell_shading(cell, cls.WISC_HEADER_FILL)
                    elif cell == row.cells[0]:
                        cls._set_cell_shading(cell, cls.WISC_NAME_FILL)
                    else:
                        cls._set_cell_shading(cell, cls.WISC_VALUE_FILL)
                elif row_index == 0:
                    cls._set_cell_shading(cell, cls.HEADER_FILL)
                for paragraph in cell.paragraphs:
                    paragraph.alignment = (
                        WD_ALIGN_PARAGRAPH.CENTER
                        if row_index == 0
                        else WD_ALIGN_PARAGRAPH.LEFT
                    )
                    paragraph.paragraph_format.space_after = Pt(0)
                    paragraph.paragraph_format.line_spacing = 1.5
                    for run in paragraph.runs:
                        run.font.name = cls.FONT_NAME
                        run.font.size = cls.TABLE_SIZE
                        if row_index == 0:
                            run.bold = True
                        if table_key == "wisc" and row_index > 0 and cell == row.cells[0]:
                            run.font.color.rgb = RGBColor(255, 255, 255)
                cell.vertical_alignment = None

            if table_key == "wisc" and row_index > 0 and row.cells[0].text == "Fala Espontânea":
                merged = row.cells[1]
                for idx in range(2, len(row.cells)):
                    merged = merged.merge(row.cells[idx])
                row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT

    @classmethod
    def _apply_table_widths(cls, table, table_key: str):
        widths_map = {
            "wisc": [
                Inches(2.35),
                Inches(1.05),
                Inches(1.05),
                Inches(1.05),
                Inches(0.95),
                Inches(1.35),
            ],
            "bpa": [Inches(2.8), Inches(1.2), Inches(1.0), Inches(1.2)],
            "ravlt": [Inches(2.2), Inches(1.2)],
            "fdt": [
                Inches(2.0),
                Inches(1.0),
                Inches(1.0),
                Inches(0.8),
                Inches(0.9),
                Inches(1.5),
            ],
            "etdah": [Inches(2.6), Inches(1.0), Inches(0.9), Inches(0.9), Inches(1.4)],
            "scared": [Inches(2.3), Inches(0.9), Inches(0.9), Inches(1.1), Inches(1.1)],
            "epq": [Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.8)],
            "srs2": [Inches(2.6), Inches(0.8), Inches(0.8), Inches(0.9), Inches(1.3)],
            "scale_summary": [Inches(2.2), Inches(3.0)],
        }
        widths = widths_map.get(table_key)
        if not widths:
            return
        for row in table.rows:
            for idx, cell in enumerate(row.cells[: len(widths)]):
                cell.width = widths[idx]

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
    def _bpa_rows(cls, test: dict | None):
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

    @classmethod
    def _ravlt_rows(cls, test: dict | None):
        payload = (
            (test or {}).get("classified_payload")
            or (test or {}).get("computed_payload")
            or {}
        )
        rows = [["Item", "Pontos Brutos"]]
        for label, key in (
            ("A1", "a1"),
            ("A2", "a2"),
            ("A3", "a3"),
            ("A4", "a4"),
            ("A5", "a5"),
            ("B1", "b1"),
            ("A6", "a6"),
            ("A7", "a7"),
            ("R", "r"),
            ("ALT", "alt"),
            ("RET", "ret"),
            ("I.P.", "ip"),
            ("I.R.", "ir"),
        ):
            value = payload.get(key)
            if value is None and key == "b1":
                value = payload.get("b")
            if value is not None:
                rows.append([label, cls._num(value)])
        return rows if len(rows) > 1 else None

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
                "Percentil",
                "Classificação",
            ]
        ]
        for item in payload.get("metric_results") or []:
            err = errors.get((item.get("codigo") or "").lower(), {})
            rows.append(
                [
                    item.get("nome") or item.get("codigo") or "-",
                    cls._num(item.get("media")),
                    cls._num(item.get("valor")),
                    cls._num(err.get("qtde_erros")),
                    cls._num(item.get("percentil_num")),
                    item.get("classificacao")
                    or err.get("classificacao_guilmette")
                    or "-",
                ]
            )
        return rows if len(rows) > 1 else None

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
        rows = [["Escala", "Bruto", "T-Score", "Percentil", "Classificação"]]
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
        bold_font = None
        if cls.LOCAL_LIBERATION_SERIF.exists():
            font_manager.fontManager.addfont(str(cls.LOCAL_LIBERATION_SERIF))
            regular_font = font_manager.FontProperties(fname=str(cls.LOCAL_LIBERATION_SERIF))
        if cls.LOCAL_LIBERATION_SERIF_BOLD.exists():
            font_manager.fontManager.addfont(str(cls.LOCAL_LIBERATION_SERIF_BOLD))
            bold_font = font_manager.FontProperties(fname=str(cls.LOCAL_LIBERATION_SERIF_BOLD))
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

        fig, ax = plt.subplots(figsize=(11, 6), dpi=150)
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        bands = [
            (130, 160, "#b8d87a"),
            (120, 130, "#c8e08a"),
            (110, 120, "#d8e8a0"),
            (90, 110, "#c8d8e8"),
            (80, 90, "#f0f0a0"),
            (70, 80, "#f0f000"),
            (40, 70, "#f0d080"),
        ]
        for y0, y1, color in bands:
            ax.axhspan(y0, y1, facecolor=color, alpha=1.0, zorder=0)

        ax.set_ylim(40, 160)
        ax.set_xlim(-0.5, len(labels) - 0.5)
        ax.yaxis.set_major_locator(plt.MultipleLocator(10))
        ax.grid(axis="y", color="white", linewidth=1.2, zorder=1)
        ax.grid(axis="x", color="white", linewidth=1.2, zorder=1)
        ax.set_axisbelow(True)

        color_by_label = {
            "ICV": "#4472C4",
            "IOP": "#ED7D31",
            "IMO": "#808080",
            "IVP": "#FFC000",
            "QI Total": "#70AD47",
            "GAI": "#4472C4",
            "CPI": "#843C0C",
        }
        colors = [color_by_label.get(label, "#5B9BD5") for label in labels]

        bars = ax.bar(
            x,
            values,
            width=0.62,
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
            elinewidth=1.8,
            capsize=6,
            capthick=1.8,
            zorder=4,
        )

        for xi, value in zip(x, values):
            ax.text(
                xi,
                42,
                cls._num(value),
                ha="center",
                va="bottom",
                fontsize=11,
                fontweight="bold",
                color="white",
                fontproperties=bold_font,
                zorder=4,
            )

        ax.set_title(
            "WISC-IV INDICES QIs",
            color="#70AD47",
            pad=12,
            fontproperties=title_font or regular_font,
            fontweight="normal",
        )
        ax.set_ylabel(
            "Pontos Compostos",
            color="#3a5a1a",
            fontproperties=y_label_font or regular_font,
        )
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=10, fontproperties=x_label_font or regular_font)
        ax.tick_params(axis="y", labelsize=10, colors="#555555")
        ax.tick_params(axis="x", pad=4, colors="#555555")
        if y_tick_font:
            for label in ax.get_yticklabels():
                label.set_fontproperties(y_tick_font)

        ax.spines["left"].set_color("#aaaaaa")
        ax.spines["bottom"].set_color("#aaaaaa")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        output = BytesIO()
        plt.tight_layout()
        fig.savefig(output, format="png", bbox_inches="tight", facecolor="white")
        plt.close(fig)
        return output.getvalue()

    @classmethod
    def _wisc_chart(cls, test: dict | None):
        payload = (test or {}).get("classified_payload") or {}
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
    def _bpa_chart(cls, test: dict | None):
        payload = (test or {}).get("classified_payload") or {}
        labels = [
            item.get("codigo", "").upper() for item in payload.get("subtestes") or []
        ]
        values = [
            float(item.get("percentil") or 0) for item in payload.get("subtestes") or []
        ]
        return cls._build_chart_png(
            "bar", "Perfil atencional no BPA-2", labels, values, "Percentil"
        )

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
