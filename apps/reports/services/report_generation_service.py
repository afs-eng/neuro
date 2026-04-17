from django.utils import timezone

from apps.evaluations.models import EvaluationStatus
from apps.reports.models import Report, ReportSection, ReportStatus
from apps.reports.services.report_ai_service import ReportAIService
from apps.reports.services.report_context_service import ReportContextService
from apps.reports.services.report_review_service import ReportReviewService
from apps.reports.services.section_registry import (
    get_section_config,
    list_section_configs,
)
from apps.reports.services.report_version_service import ReportVersionService


class ReportGenerationService:
    AI_FALLBACK_WARNING = "A IA nao esta disponivel no momento; o texto foi gerado pelo fallback deterministico."

    SECTION_GROUPS = {
        "capacidade_cognitiva_global": {"eficiencia_intelectual"},
        "linguagem": {"linguagem"},
        "gnosias_praxias": {"gnosias_praxias"},
        "atencao": {"atencao"},
        "memoria_aprendizagem": {"memoria_aprendizagem"},
        "funcoes_executivas": {"funcoes_executivas"},
        "aspectos_emocionais_comportamentais": {"escalas_complementares"},
    }

    @staticmethod
    def construct_clinical_context(evaluation):
        return ReportContextService.build_context(evaluation)

    @staticmethod
    def get_sections_config():
        return [(key, config["title"]) for key, config in list_section_configs()]

    @classmethod
    def _has_test(cls, context: dict, *codes: str) -> bool:
        available = {
            item.get("instrument_code") for item in context.get("validated_tests") or []
        }
        return any(code in available for code in codes)

    @classmethod
    def _enabled_sections_config(cls, context: dict):
        is_adolescent = cls._is_adolescent_case(context)
        base = []
        for key, title in cls.get_sections_config():
            config = get_section_config(key)
            required_any_codes = tuple(config.get("required_any_codes") or ())
            enabled = True
            if required_any_codes:
                enabled = cls._has_test(context, *required_any_codes)
            if not enabled and config.get("enable_when_adolescent"):
                enabled = is_adolescent
            if enabled:
                base.append((key, title))
        renumbered = []
        for index, (key, title) in enumerate(base, start=1):
            clean_title = title.split(". ", 1)[1] if ". " in title else title
            renumbered.append((key, f"{index}. {clean_title}"))
        return renumbered

    @classmethod
    def generate_full_report(cls, report: Report, user=None):
        report.status = ReportStatus.GENERATING
        report.save(update_fields=["status", "updated_at"])

        context = cls.construct_clinical_context(report.evaluation)
        report.context_payload = context
        if not report.interested_party:
            report.interested_party = context["patient"]["full_name"]
        if not report.purpose:
            report.purpose = (
                context["evaluation"].get("evaluation_purpose")
                or context["evaluation"].get("referral_reason")
                or "Auxílio diagnóstico e planejamento clínico."
            )

        sections_config = cls._enabled_sections_config(context)
        full_markdown_text = []
        ai_sections = []
        fallback_sections = []

        report.sections.exclude(key__in=[key for key, _ in sections_config]).delete()

        for order, (key, title) in enumerate(sections_config):
            generated_content, generation_metadata, warnings = (
                cls._generate_section_payload(report, key, context)
            )
            if generation_metadata.get("provider") in {"ollama", "openai", "anthropic"}:
                ai_sections.append(key)
            else:
                fallback_sections.append(key)
            ReportSection.objects.update_or_create(
                report=report,
                key=key,
                defaults={
                    "title": title,
                    "order": order,
                    "content_generated": generated_content,
                    "content_edited": generated_content,
                    "generation_metadata": generation_metadata,
                    "warnings_payload": warnings,
                },
            )
            full_markdown_text.append(f"# {title}\n\n{generated_content}")

        report.generated_text = "\n\n".join(full_markdown_text)
        report.edited_text = report.generated_text
        report.status = ReportStatus.IN_REVIEW
        report.generated_at = timezone.now()
        report.ai_metadata = {
            "mode": "hybrid"
            if ai_sections and fallback_sections
            else ("ai" if ai_sections else "deterministic"),
            "ai_sections": ai_sections,
            "fallback_sections": fallback_sections,
        }
        report.ai_metadata["review"] = ReportReviewService.review(report)
        report.save(
            update_fields=[
                "context_payload",
                "interested_party",
                "purpose",
                "generated_text",
                "edited_text",
                "ai_metadata",
                "status",
                "generated_at",
                "updated_at",
            ]
        )

        ReportVersionService.create_version(report, user=user)

        report.evaluation.status = EvaluationStatus.WRITING_REPORT
        report.evaluation.save(update_fields=["status"])
        return report

    @classmethod
    def _generate_section_payload(cls, report: Report, key: str, context: dict):
        if ReportAIService.supports_section(key):
            try:
                generation_result = ReportAIService.generate_section(
                    report, key, context
                )
                content = generation_result.get("content") or ""
                if content.strip():
                    return (
                        content,
                        generation_result.get("metadata") or {},
                        generation_result.get("warnings") or [],
                    )
            except Exception as exc:
                fallback_content = cls._generate_section_text(report, key, context)
                return (
                    fallback_content,
                    {
                        "provider": "deterministic",
                        "model": "rules-based",
                        "section": key,
                        "fallback_reason": str(exc),
                        "used_fallback": True,
                        "generation_path": "deterministic_fallback",
                    },
                    [cls.AI_FALLBACK_WARNING],
                )

        return (
            cls._generate_section_text(report, key, context),
            {
                "provider": "deterministic",
                "model": "rules-based",
                "section": key,
                "used_fallback": False,
                "generation_path": "deterministic_only",
            },
            [],
        )

    @staticmethod
    def _format_sex(value: str | None) -> str:
        if not value:
            return "Não informado"
        mapping = {"M": "Masculino", "F": "Feminino", "O": "Outro"}
        return mapping.get(value, value)

    @staticmethod
    def _format_date(value: str | None) -> str:
        if not value:
            return "Não informado"
        try:
            year, month, day = value.split("-")
            return f"{day}/{month}/{year}"
        except ValueError:
            return value

    @staticmethod
    def _format_age(context: dict) -> str:
        birth_date = context["patient"].get("birth_date")
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
    def _age_years(context: dict) -> int | None:
        birth_date = context["patient"].get("birth_date")
        if not birth_date:
            return None
        try:
            from datetime import date

            year, month, day = map(int, birth_date.split("-"))
            born = date(year, month, day)
            today = date.today()
            return (
                today.year
                - born.year
                - ((today.month, today.day) < (born.month, born.day))
            )
        except ValueError:
            return None

    @staticmethod
    def _build_filiation(patient: dict) -> str:
        names = [patient.get("father_name"), patient.get("mother_name")]
        names = [
            name.strip() for name in names if isinstance(name, str) and name.strip()
        ]
        if names:
            return " e ".join(names)
        if patient.get("responsible_name"):
            return str(patient.get("responsible_name"))
        return "Não informada"

    @classmethod
    def _is_adolescent_case(cls, context: dict) -> bool:
        template_code = (
            (context.get("anamnesis") or {}).get("current_response") or {}
        ).get("template_code") or ""
        age = cls._age_years(context)
        return "adolescent" in template_code or (age is not None and 12 <= age < 18)

    @staticmethod
    def _answers_payload(context: dict) -> dict:
        return ((context.get("anamnesis") or {}).get("current_response") or {}).get(
            "answers_payload"
        ) or {}

    @classmethod
    def _pick_answer(cls, context: dict, *keys: str) -> str:
        answers = cls._answers_payload(context)
        for key in keys:
            value = answers.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
            if isinstance(value, (int, float)):
                return str(value)
            if isinstance(value, list) and value:
                parts = [str(item).strip() for item in value if str(item).strip()]
                if parts:
                    return "; ".join(parts)
        return ""

    @classmethod
    def _adolescent_history_sections(cls, context: dict) -> list[tuple[str, str]]:
        sections = [
            (
                "Gestação e parto",
                cls._pick_answer(context, "pregnancy_birth_intercurrences"),
            ),
            (
                "Desenvolvimento motor",
                cls._pick_answer(context, "motor_development_notes", "motor_delay"),
            ),
            (
                "Desenvolvimento linguístico",
                cls._pick_answer(
                    context, "language_development_notes", "language_delay"
                ),
            ),
            (
                "Desenvolvimento socioemocional",
                cls._pick_answer(
                    context,
                    "social_emotional_development",
                    "relationship_mother",
                    "relationship_father",
                    "relationship_siblings",
                ),
            ),
            (
                "Histórico médico",
                cls._pick_answer(
                    context, "medical_history", "medical_notes", "medical_specialties"
                ),
            ),
            (
                "Sono e alimentação",
                cls._pick_answer(context, "sleep_pattern", "eating_pattern"),
            ),
            (
                "Histórico educacional",
                cls._pick_answer(
                    context,
                    "school_history",
                    "learning_difficulties",
                    "school_observations",
                ),
            ),
            (
                "Rotina atual",
                cls._pick_answer(
                    context, "daily_routine", "screen_time", "leisure_activities"
                ),
            ),
            (
                "Informações adicionais",
                cls._pick_answer(context, "additional_notes", "current_main_concern"),
            ),
        ]
        return [(title, text) for title, text in sections if text]

    @classmethod
    def _procedure_lines(cls, context: dict) -> list[str]:
        entries = context.get("progress_entries") or []
        session_count = max(len(entries), 1)
        current_response = (context.get("anamnesis") or {}).get(
            "current_response"
        ) or {}
        devolutiva = current_response.get("submitted_by_name") or cls._pick_answer(
            context, "primary_guardian", "submitted_by_name"
        )
        lines = [
            f"Para esta avaliação foram realizadas: uma sessão de anamnese, {session_count:02d} sessões de testagem e uma sessão de devolutiva{' com ' + devolutiva if devolutiva else ''}.",
            "Anamnese estruturada, observação clínica e análise documental foram utilizadas como fontes complementares.",
        ]
        for test in context.get("validated_tests") or []:
            instrument = (
                test.get("instrument_name") or test.get("instrument") or "Instrumento"
            )
            summary = (
                test.get("summary")
                or test.get("clinical_interpretation")
                or "Utilizado para composição clínica do caso."
            )
            lines.append(f"{instrument}: {summary}")
        return lines

    @staticmethod
    def _anamnesis_summary(context: dict) -> str:
        payload = context.get("anamnesis", {}).get("current_response") or {}
        summary_payload = payload.get("summary_payload") or {}
        if isinstance(summary_payload, dict):
            values = [str(value).strip() for value in summary_payload.values() if value]
            if values:
                return " ".join(values[:3])
        answers = payload.get("answers_payload") or {}
        if isinstance(answers, dict):
            values = [
                str(value).strip()
                for value in answers.values()
                if isinstance(value, (str, int, float)) and value
            ]
            if values:
                return " ".join(values[:4])
        return "Não houve anamnese estruturada suficiente registrada até o momento da geração do laudo."

    @staticmethod
    def _progress_summary(context: dict) -> str:
        entries = context.get("progress_entries") or []
        if not entries:
            return "Não há registros evolutivos incluídos no laudo até o momento."
        parts = []
        for entry in entries[:3]:
            chunk = " ".join(
                filter(
                    None,
                    [
                        entry.get("objective", ""),
                        entry.get("observed_behavior", ""),
                        entry.get("clinical_notes", ""),
                        entry.get("next_steps", ""),
                    ],
                )
            ).strip()
            if chunk:
                parts.append(chunk)
        return (
            " ".join(parts)
            if parts
            else "Há registros evolutivos, porém sem síntese clínica adicional."
        )

    @classmethod
    def _tests_for_section(cls, context: dict, section_key: str) -> list[dict]:
        target_sections = cls.SECTION_GROUPS.get(section_key, set())
        tests = context.get("validated_tests") or []
        filtered = [
            test for test in tests if test.get("report_section") in target_sections
        ]
        if filtered:
            return filtered
        if section_key in {
            "linguagem",
            "gnosias_praxias",
            "capacidade_cognitiva_global",
        }:
            return [
                test
                for test in tests
                if test.get("instrument_code") in {"wisc4", "wasi", "wais3"}
            ]
        return filtered

    @staticmethod
    def _tests_bullet_list(tests: list[dict]) -> str:
        if not tests:
            return (
                "Nenhum instrumento específico deste domínio foi validado na avaliação."
            )
        lines = []
        for test in tests:
            summary = (
                test.get("summary")
                or test.get("clinical_interpretation")
                or "Sem interpretação clínica consolidada."
            )
            lines.append(f"- {test.get('instrument_name')}: {summary}")
        return "\n".join(lines)

    @staticmethod
    def _tests_detailed_blocks(tests: list[dict]) -> str:
        if not tests:
            return (
                "Nenhum instrumento específico deste domínio foi validado na avaliação."
            )

        blocks = []
        for test in tests:
            lines = [f"Instrumento: {test.get('instrument_name')}"]
            if test.get("applied_on"):
                lines.append(
                    f"Data de aplicação: {ReportGenerationService._format_date(test.get('applied_on'))}"
                )

            result_rows = test.get("result_rows") or []
            if result_rows:
                lines.append("Resultados estruturados:")
                lines.extend(result_rows)

            interpretation = test.get("clinical_interpretation") or test.get("summary")
            if interpretation:
                lines.append(f"Interpretação clínica: {interpretation}")

            for warning in test.get("warnings") or []:
                lines.append(f"Observação técnica: {warning}")

            blocks.append("\n".join(lines))

        return "\n\n".join(blocks)

    @staticmethod
    def _document_summary(context: dict) -> str:
        documents = context.get("documents") or []
        if not documents:
            return "Não foram anexados documentos complementares relevantes para composição do laudo."
        return "; ".join(
            f"{item.get('title')} ({item.get('document_type_display') or item.get('document_type')})"
            for item in documents[:5]
        )

    @classmethod
    def _generate_section_text(cls, report: Report, key: str, context: dict) -> str:
        patient = context["patient"]
        evaluation = context["evaluation"]
        is_adolescent = cls._is_adolescent_case(context)
        professional = (
            report.author.display_name if report.author else "Profissional responsável"
        )

        if key == "identificacao":
            interested_party = report.interested_party or patient["full_name"]
            if (
                patient.get("responsible_name")
                and interested_party == patient["full_name"]
            ):
                interested_party = patient.get("responsible_name")
            return "\n".join(
                [
                    "1.1. Identificação do laudo:",
                    f"Autora: {professional}",
                    f"Interessado: {interested_party}",
                    f"Finalidade: {report.purpose or 'Auxílio diagnóstico e planejamento clínico.'}",
                    "",
                    "1.2. Identificação do paciente:",
                    f"Nome: {patient['full_name']}",
                    f"Sexo: {cls._format_sex(patient.get('sex'))}",
                    f"Data de nascimento: {cls._format_date(patient.get('birth_date'))}",
                    f"Idade: {cls._format_age(context)}",
                    f"Filiação: {cls._build_filiation(patient)}",
                    f"Escolaridade: {patient.get('schooling') or 'Não informada'}",
                ]
            )

        if key == "descricao_demanda":
            if is_adolescent:
                referral_source = cls._pick_answer(context, "referral_source")
                main_complaint = cls._pick_answer(context, "main_complaint")
                main_contexts = cls._pick_answer(context, "main_contexts")
                concern = cls._pick_answer(context, "current_main_concern")
                goal = cls._pick_answer(context, "evaluation_goal")
                parts = []
                if referral_source:
                    parts.append(f"O adolescente foi encaminhado por {referral_source}")
                else:
                    parts.append(
                        "O adolescente foi encaminhado para avaliação neuropsicológica"
                    )
                parts.append(
                    f"em razão de {evaluation.get('referral_reason') or main_complaint or 'queixas cognitivas, emocionais e escolares em investigação clínica'}."
                )
                if main_contexts:
                    parts.append(
                        f"As dificuldades são descritas sobretudo no contexto {main_contexts}."
                    )
                if concern:
                    parts.append(
                        f"A principal preocupação atual refere-se a {concern}."
                    )
                parts.append(
                    f"A finalidade clínica da avaliação é {report.purpose or goal or evaluation.get('evaluation_purpose') or 'auxiliar o raciocínio diagnóstico, o planejamento terapêutico e a orientação familiar e escolar'}."
                )
                return " ".join(parts)
            return (
                f"A avaliação neuropsicológica foi solicitada em razão de {evaluation.get('referral_reason') or 'queixas cognitivas e comportamentais em investigação clínica'}. "
                f"A finalidade principal do processo é {report.purpose or evaluation.get('evaluation_purpose') or 'subsidiar o raciocínio diagnóstico e o planejamento terapêutico'}. "
                "O presente laudo considera as informações disponíveis no contexto clínico estruturado, integrando entrevista, registros evolutivos, documentos e resultados dos testes já validados."
            )

        if key == "procedimentos":
            if is_adolescent:
                return "\n".join(cls._procedure_lines(context))
            test_list = cls._tests_bullet_list(context.get("validated_tests") or [])
            return "\n".join(
                [
                    "Para a presente avaliação foram considerados os seguintes procedimentos e fontes de informação:",
                    "- Entrevista/anamnese estruturada.",
                    "- Registros de evolução clínica incluídos no laudo.",
                    f"- Documentos complementares: {cls._document_summary(context)}.",
                    "- Instrumentos psicológicos/neuropsicológicos validados:",
                    test_list,
                    f"- Total de registros evolutivos incluídos: {len(context.get('progress_entries') or [])}.",
                ]
            )

        if key == "historia_pessoal":
            if is_adolescent:
                adolescent_sections = cls._adolescent_history_sections(context)
                if adolescent_sections:
                    return "\n\n".join(
                        f"{title}: {text}" for title, text in adolescent_sections
                    )
            return (
                f"{cls._anamnesis_summary(context)} "
                f"Registros evolutivos relevantes: {cls._progress_summary(context)}"
            )

        if key in cls.SECTION_GROUPS:
            tests = cls._tests_for_section(context, key)
            intro_map = {
                "capacidade_cognitiva_global": "A análise da capacidade cognitiva global foi baseada nos instrumentos com maior sensibilidade para estimativa do funcionamento intelectual e raciocínio geral.",
                "linguagem": "A análise da linguagem considera compreensão verbal, repertório lexical, organização semântica e impacto funcional na comunicação cotidiana e acadêmica.",
                "gnosias_praxias": "A análise de gnosias e praxias considera integração visuoespacial, raciocínio não verbal e organização construtiva.",
                "atencao": "A análise da atenção considera os sistemas atencionais sustentado, seletivo, alternado e dividido, conforme os dados já validados.",
                "memoria_aprendizagem": "A análise da memória e da aprendizagem contempla aquisição, retenção, evocação e reconhecimento, conforme os instrumentos aplicados.",
                "funcoes_executivas": "A análise das funções executivas considera controle inibitório, flexibilidade cognitiva, planejamento, monitoramento e velocidade de processamento.",
                "aspectos_emocionais_comportamentais": "A análise dos aspectos emocionais e comportamentais integra escalas complementares e observações clínicas descritas ao longo da avaliação.",
            }
            closing_map = {
                "capacidade_cognitiva_global": "Em síntese, os resultados devem ser interpretados em conjunto com os demais domínios cognitivos e com a funcionalidade observada no cotidiano.",
                "linguagem": "Os achados de linguagem precisam ser compreendidos em articulação com escolaridade, repertório sociocultural e demais funções cognitivas.",
                "gnosias_praxias": "Esses resultados contribuem para a compreensão do modo como o paciente organiza informações visuais e executa respostas motoras dirigidas a metas.",
                "atencao": "Os resultados atencionais ajudam a explicar dificuldades funcionais relativas à manutenção de foco, alternância entre demandas e organização da rotina.",
                "memoria_aprendizagem": "O perfil mnésico deve ser interpretado junto à atenção, à interferência emocional e às exigências ambientais cotidianas.",
                "funcoes_executivas": "As funções executivas influenciam diretamente o desempenho acadêmico, profissional e adaptativo, especialmente em contextos complexos e pouco estruturados.",
                "aspectos_emocionais_comportamentais": "Os aspectos emocionais e comportamentais podem atuar como fatores moduladores do desempenho cognitivo observado na avaliação.",
            }
            return "\n".join(
                [
                    intro_map[key],
                    "",
                    cls._tests_detailed_blocks(tests),
                    "",
                    closing_map[key],
                ]
            )

        if key == "bpa2":
            tests = [
                test
                for test in context.get("validated_tests") or []
                if test.get("instrument_code") == "bpa2"
            ]
            return "\n".join(
                [
                    "A BPA-2 foi utilizada para mensurar atenção concentrada, dividida, alternada e capacidade geral de atenção.",
                    "",
                    cls._tests_detailed_blocks(tests),
                    "",
                    "Em análise clínica, o desempenho atencional deve ser integrado às demandas escolares, ao ritmo de trabalho mental e às observações comportamentais registradas nas sessões.",
                ]
            )

        if key == "ravlt":
            tests = [
                test
                for test in context.get("validated_tests") or []
                if test.get("instrument_code") == "ravlt"
            ]
            return "\n".join(
                [
                    "O RAVLT foi utilizado para investigar memória auditivo-verbal, curva de aprendizagem, interferência e retenção tardia.",
                    "",
                    cls._tests_detailed_blocks(tests),
                    "",
                    "A leitura clínica considera não apenas o escore bruto, mas também a forma como o paciente aprende, mantém e recupera informações ao longo da tarefa.",
                ]
            )

        if key == "fdt":
            tests = [
                test
                for test in context.get("validated_tests") or []
                if test.get("instrument_code") == "fdt"
            ]
            return "\n".join(
                [
                    "O FDT permite observar processos automáticos e controlados, com ênfase em velocidade de processamento, inibição e flexibilidade cognitiva.",
                    "",
                    cls._tests_detailed_blocks(tests),
                    "",
                    "Em análise clínica, tempos elevados e aumento de erros em tarefas controladas sugerem maior custo executivo, especialmente em situações de mudança de regra e monitoramento da resposta.",
                ]
            )

        if key == "etdah_pais":
            tests = [
                test
                for test in context.get("validated_tests") or []
                if test.get("instrument_code") == "etdah_pais"
            ]
            return "\n".join(
                [
                    "A escala E-TDAH-PAIS contribui para compreender a percepção dos responsáveis acerca de atenção, impulsividade, comportamento adaptativo e regulação emocional.",
                    "",
                    cls._tests_detailed_blocks(tests),
                    "",
                    "Os resultados devem ser correlacionados com a observação clínica direta e com o funcionamento do adolescente em casa e na escola.",
                ]
            )

        if key == "etdah_ad":
            tests = [
                test
                for test in context.get("validated_tests") or []
                if test.get("instrument_code") == "etdah_ad"
            ]
            return "\n".join(
                [
                    "A escala E-TDAH-AD oferece a perspectiva do próprio adolescente sobre desatenção, hiperatividade, impulsividade e aspectos emocionais associados.",
                    "",
                    cls._tests_detailed_blocks(tests),
                    "",
                    "A interpretação do autorrelato exige integração com o relato familiar, desempenho nos testes e observação clínica do caso.",
                ]
            )

        if key == "scared":
            tests = [
                test
                for test in context.get("validated_tests") or []
                if test.get("instrument_code") == "scared"
            ]
            return "\n".join(
                [
                    "O SCARED investiga sintomas ansiosos por domínios, permitindo identificar rastreios positivos para ansiedade generalizada, fobia social, ansiedade de separação, pânico e evitação escolar.",
                    "",
                    cls._tests_detailed_blocks(tests),
                    "",
                    "As elevações precisam ser interpretadas à luz do contexto emocional do adolescente, do repertório de enfrentamento e dos achados observacionais.",
                ]
            )

        if key == "srs2":
            tests = [
                test
                for test in context.get("validated_tests") or []
                if test.get("instrument_code") == "srs2"
            ]
            return "\n".join(
                [
                    "O SRS-2 contribui para a investigação do funcionamento social, cognição social e padrões restritos ou repetitivos, sem substituir a integração clínica ampla do caso.",
                    "",
                    cls._tests_detailed_blocks(tests),
                    "",
                    "Os achados devem ser correlacionados com adaptação social, linguagem pragmática, ansiedade e funcionamento cognitivo global antes de qualquer formulação diagnóstica.",
                ]
            )

        if key == "epq_j":
            tests = [
                test
                for test in context.get("validated_tests") or []
                if test.get("instrument_code") == "epq_j"
            ]
            return "\n".join(
                [
                    "O EPQ-J descreve traços de personalidade em dimensões como psicoticismo, extroversão, neuroticismo e sinceridade/socialização.",
                    "",
                    cls._tests_detailed_blocks(tests),
                    "",
                    "O perfil de personalidade deve ser lido como dado complementar, articulado com ansiedade, recursos adaptativos e contexto relacional do adolescente.",
                ]
            )

        if key == "ebadep":
            tests = [
                test
                for test in context.get("validated_tests") or []
                if test.get("instrument_code") in {"ebadep_a", "ebadep_ij", "ebaped_ij"}
            ]
            return "\n".join(
                [
                    "A EBADEP auxilia na investigação de sintomas depressivos e seu possível impacto no humor, motivação, engajamento e funcionalidade global.",
                    "",
                    cls._tests_detailed_blocks(tests),
                    "",
                    "Os resultados devem ser sempre compreendidos em conjunto com a história clínica, comorbidades e contexto psicossocial atual.",
                ]
            )

        if key == "conclusao":
            validated_tests = context.get("validated_tests") or []
            main_domains = ", ".join(
                sorted({item.get("domain") or "geral" for item in validated_tests})
            )
            if is_adolescent:
                hypothesis = evaluation.get("clinical_hypothesis")
                return (
                    f"Considerando a integração entre anamnese, contexto familiar e escolar, observação clínica e instrumentos validados, o adolescente apresenta achados com repercussão em {main_domains or 'diferentes domínios do funcionamento cognitivo e socioemocional'}. "
                    f"A síntese clínica sugere {hypothesis or 'necessidade de investigação diagnóstica integrada e acompanhamento multiprofissional'}, correlacionando desempenho psicométrico, funcionalidade cotidiana e recursos adaptativos. "
                    "A presente conclusão não deve ser interpretada isoladamente, exigindo leitura conjunta com a história do desenvolvimento, comorbidades e resposta do adolescente às demandas ambientais."
                )
            return (
                f"Considerando a integração entre anamnese, evolução clínica, documentos e instrumentos validados, o caso sugere alterações com impacto nos domínios de {main_domains or 'funcionamento cognitivo geral'}. "
                "Os resultados não devem ser interpretados isoladamente, mas como parte de um raciocínio clínico integrado e sujeito à revisão profissional."
            )

        if key == "hipotese_diagnostica":
            hypothesis = evaluation.get("clinical_hypothesis")
            if hypothesis:
                return (
                    f"A hipótese diagnóstica preliminar registrada para o caso é: {hypothesis}. "
                    "Os achados da avaliação oferecem subsídios para discussão clínica, sem substituir a decisão diagnóstica final do profissional responsável."
                )
            return "Até o presente momento, os dados sustentam hipóteses clínicas em investigação, recomendando-se correlação com história do desenvolvimento, exames complementares e acompanhamento multiprofissional quando pertinente."

        if key == "sugestoes_conduta":
            if is_adolescent:
                return (
                    "Sugere-se devolutiva estruturada com adolescente e responsáveis, psicoeducação sobre o perfil cognitivo e emocional observado, articulação com a escola para adaptações quando necessárias e acompanhamento multiprofissional conforme as hipóteses clínicas em investigação. "
                    "Recomenda-se monitoramento longitudinal do funcionamento acadêmico, social e emocional, bem como orientação familiar para manejo das áreas de maior vulnerabilidade identificadas."
                )
            return (
                "Sugere-se devolutiva clínica estruturada ao paciente e/ou responsáveis, articulação com profissionais assistentes, e planejamento de intervenções voltadas às áreas de maior vulnerabilidade identificadas. "
                "Também se recomenda acompanhamento longitudinal para monitoramento da funcionalidade e resposta às estratégias terapêuticas adotadas."
            )

        return (
            "Seção em elaboração a partir do contexto clínico estruturado da avaliação."
        )
