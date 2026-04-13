import json

from apps.ai.guards.data_presence_guard import DataPresenceGuard
from apps.ai.services.text_generation_service import TextGenerationService


class ReportAIService:
    WISC_SECTION_SUBTEST_CODES = {
        "funcoes_executivas": {"SM", "CO", "CN", "RM", "SNL"},
        "linguagem": {"SM", "VC", "CO"},
        "gnosias_praxias": {"RM", "CB"},
        "memoria_aprendizagem": {"DG", "SNL"},
    }
    WISC_DOMAIN_SUMMARIES = {
        "funcoes_executivas": {
            "intro": "Considere apenas os subtestes do WISC-IV ligados a planejamento, abstração, monitoramento cognitivo, flexibilidade mental, controle inibitório e resolução de problemas.",
            "preserved": "Os achados sugerem funcionamento executivo globalmente preservado, com recursos adequados para organização do pensamento, abstração e manejo de demandas cognitivas mais complexas.",
            "mixed": "Os achados sugerem perfil executivo heterogêneo, com áreas preservadas e fragilidades relativas em componentes específicos do funcionamento executivo.",
            "low": "Os achados sugerem fragilidades no funcionamento executivo, com possível repercussão sobre planejamento, controle mental, flexibilidade cognitiva e organização do comportamento dirigido a objetivos.",
        },
        "linguagem": {
            "intro": "Considere apenas os subtestes do WISC-IV ligados a compreensão verbal, abstração mediada pela linguagem, repertório lexical e uso funcional da linguagem.",
            "preserved": "Os achados sugerem funcionamento linguístico preservado, com repertório verbal compatível com a faixa etária e recursos adequados para compreensão, expressão e elaboração conceitual.",
            "mixed": "Os achados sugerem perfil linguístico relativamente heterogêneo, com preservação de alguns componentes da linguagem e fragilidades pontuais em outros aspectos do processamento verbal.",
            "low": "Os achados sugerem fragilidades no domínio da linguagem, com possível impacto sobre compreensão verbal, abstração conceitual, repertório lexical e uso funcional da linguagem.",
        },
        "gnosias_praxias": {
            "intro": "Considere apenas os subtestes do WISC-IV ligados a percepção visual, organização visuoespacial e integração visuoconstrutiva.",
            "preserved": "Os achados sugerem funcionamento preservado em gnosias e praxias, com recursos adequados para análise perceptual, organização espacial e execução visuoconstrutiva.",
            "mixed": "Os achados sugerem perfil misto, com habilidades perceptuais relativamente preservadas, mas com fragilidades em componentes específicos da organização visuoespacial e da praxia construtiva.",
            "low": "Os achados sugerem fragilidades em gnosias e praxias, com possível repercussão sobre organização visuoespacial, percepção de relações espaciais, planejamento construtivo e execução motora organizada.",
        },
        "memoria_aprendizagem": {
            "intro": "Considere apenas os subtestes do WISC-IV ligados a retenção imediata, memória operacional e manipulação mental de informações, integrando com outros instrumentos mnésicos quando existirem.",
            "preserved": "Os achados sugerem funcionamento preservado da memória e da aprendizagem, com recursos adequados para retenção, manipulação mental e consolidação de informações.",
            "mixed": "Os achados sugerem perfil heterogêneo, com preservação de alguns processos mnésicos e fragilidades relativas em componentes específicos da aprendizagem e da recuperação de informações.",
            "low": "Os achados sugerem fragilidades nos processos de memória e aprendizagem, com possível impacto sobre retenção ativa de informações, evocação e desempenho em tarefas que exigem aquisição progressiva de conteúdo.",
        },
    }

    TEST_GENERATORS = {
        "bpa2": {
            "prompt": "reports/bpa2_prompt.txt",
            "codes": {"bpa2"},
            "kind": "test",
            "timeout": 1200,
        },
        "fdt": {
            "prompt": "reports/fdt_prompt.txt",
            "codes": {"fdt"},
            "kind": "test",
            "timeout": 1200,
        },
        "ravlt": {
            "prompt": "reports/ravlt_prompt.txt",
            "codes": {"ravlt"},
            "kind": "test",
            "timeout": 1200,
        },
        "etdah_pais": {
            "prompt": "reports/etdah_pais_prompt.txt",
            "codes": {"etdah_pais"},
            "kind": "test",
            "timeout": 1500,
        },
        "etdah_ad": {
            "prompt": "reports/etdah_ad_prompt.txt",
            "codes": {"etdah_ad"},
            "kind": "test",
            "timeout": 1500,
        },
        "scared": {
            "prompt": "reports/scared_prompt.txt",
            "codes": {"scared"},
            "kind": "test",
            "timeout": 1500,
        },
        "epq_j": {
            "prompt": "reports/epq_j_prompt.txt",
            "codes": {"epq_j"},
            "kind": "test",
            "timeout": 1500,
        },
        "srs2": {
            "prompt": "reports/srs2_prompt.txt",
            "codes": {"srs2"},
            "kind": "test",
            "timeout": 1500,
        },
        "ebadep": {
            "prompt": "reports/ebadep_prompt.txt",
            "codes": {"ebadep_a", "ebadep_ij", "ebaped_ij"},
            "kind": "test",
            "timeout": 1800,
        },
    }
    SECTION_GENERATORS = {
        "atencao": {
            "prompt": "reports/attention_prompt.txt",
            "codes": {"bpa2", "etdah_ad", "etdah_pais"},
            "kind": "section",
            "timeout": 1800,
        },
        "funcoes_executivas": {
            "prompt": "reports/funcoes_executivas_prompt.txt",
            "codes": {"fdt", "wisc4", "wasi", "wais3"},
            "kind": "section",
            "timeout": 1800,
        },
        "linguagem": {
            "prompt": "reports/linguagem_prompt.txt",
            "codes": {"wisc4", "wasi", "wais3"},
            "kind": "section",
            "timeout": 1800,
        },
        "gnosias_praxias": {
            "prompt": "reports/gnosias_praxias_prompt.txt",
            "codes": {"wisc4", "wasi", "wais3"},
            "kind": "section",
            "timeout": 1800,
        },
        "memoria_aprendizagem": {
            "prompt": "reports/memoria_aprendizagem_prompt.txt",
            "codes": {"ravlt", "wisc4"},
            "kind": "section",
            "timeout": 1800,
        },
        "capacidade_cognitiva_global": {
            "prompt": "reports/capacidade_cognitiva_global_prompt.txt",
            "codes": {"wisc4", "wasi", "wais3"},
            "kind": "section",
            "timeout": 1800,
        },
        "aspectos_emocionais_comportamentais": {
            "prompt": "reports/aspectos_emocionais_comportamentais_prompt.txt",
            "codes": {
                "etdah_pais",
                "etdah_ad",
                "scared",
                "srs2",
                "epq_j",
                "ebadep_a",
                "ebadep_ij",
                "ebaped_ij",
            },
            "kind": "section",
            "timeout": 2400,
        },
    }
    SUPPORTED_SECTIONS = set(TEST_GENERATORS) | set(SECTION_GENERATORS)

    @classmethod
    def supports_section(cls, section_key: str) -> bool:
        return section_key in cls.SUPPORTED_SECTIONS

    @classmethod
    def generate_section(cls, report, section_key: str, context: dict) -> dict:
        if not cls.supports_section(section_key):
            raise ValueError(f"Secao nao suportada por IA nesta fase: {section_key}")

        return cls._generate_with_prompt(report, section_key, context)

    @classmethod
    def _generate_with_prompt(cls, report, section_key: str, context: dict) -> dict:
        warnings = DataPresenceGuard.validate_section_context(section_key, context)
        if warnings:
            raise ValueError(warnings[0])

        filtered_context = cls._build_section_context(report, section_key, context)
        config = cls._generator_config(section_key)
        result = TextGenerationService.generate_from_prompt(
            prompt_name=cls._prompt_name(section_key),
            user_prompt=cls._build_user_prompt(filtered_context),
            timeout=config["timeout"],
        )

        content = (result.get("content") or "").strip()
        if not content:
            raise ValueError(
                "A IA retornou uma resposta vazia para a secao solicitada."
            )

        return {
            "content": content,
            "warnings": result.get("warnings") or [],
            "metadata": {
                "provider": result.get("provider"),
                "model": result.get("model"),
                "finish_reason": result.get("finish_reason"),
                "usage": result.get("usage") or {},
                "section": section_key,
            },
        }

    @classmethod
    def _prompt_name(cls, section_key: str) -> str:
        config = cls._generator_config(section_key)
        return config["prompt"]

    @classmethod
    def _build_user_prompt(cls, filtered_context: dict) -> str:
        return (
            "Baseie a redacao prioritariamente nas interpretacoes tecnicas ja geradas "
            "pelos interpreters.py do sistema e persistidas em 'clinical_interpretation' ou 'technical_basis'. "
            "Use os resultados estruturados apenas para sustentar e organizar essa redacao, "
            "sem recalcular classificacoes.\n\n"
            "Dados clinicos estruturados para a secao solicitada:\n"
            f"{json.dumps(filtered_context, ensure_ascii=False, indent=2)}"
        )

    @classmethod
    def _build_section_context(cls, report, section_key: str, context: dict) -> dict:
        patient = context.get("patient") or {}
        evaluation = context.get("evaluation") or {}
        tests = context.get("validated_tests") or []
        config = cls._generator_config(section_key)
        include_structured_results = config["kind"] == "test"

        filtered_tests = [
            cls._build_test_payload(item, section_key, include_structured_results)
            for item in tests
            if item.get("instrument_code") in config["codes"]
        ]

        progress_entries = [
            {
                "entry_type": item.get("entry_type"),
                "objective": item.get("objective") or "",
                "observed_behavior": item.get("observed_behavior") or "",
                "clinical_notes": item.get("clinical_notes") or "",
            }
            for item in (context.get("progress_entries") or [])[:3]
        ]

        if config["kind"] == "test":
            return {
                "section": section_key,
                "section_kind": config["kind"],
                "report_rules": {
                    "report_language": "pt-BR",
                    "clinical_style": "tecnico_objetivo",
                    "use_first_name_only": True,
                },
                "patient": {
                    "first_name": (patient.get("full_name") or "").split(" ", 1)[0],
                    "sex": patient.get("sex"),
                },
                "evaluation": {
                    "referral_reason": evaluation.get("referral_reason") or "",
                    "evaluation_purpose": evaluation.get("evaluation_purpose") or "",
                },
                "validated_tests": filtered_tests,
            }

        return {
            "section": section_key,
            "section_kind": config["kind"],
            "report_rules": {
                "report_language": "pt-BR",
                "clinical_style": "tecnico_objetivo",
                "use_first_name_only": True,
            },
            "patient": {
                "first_name": (patient.get("full_name") or "").split(" ", 1)[0],
                "age": patient.get("birth_date"),
                "sex": patient.get("sex"),
                "schooling": patient.get("schooling"),
            },
            "evaluation": {
                "referral_reason": evaluation.get("referral_reason") or "",
                "evaluation_purpose": evaluation.get("evaluation_purpose") or "",
                "clinical_hypothesis": evaluation.get("clinical_hypothesis") or "",
            },
            "anamnesis": (context.get("anamnesis") or {}).get("current_response") or {},
            "progress_entries": progress_entries,
            "validated_tests": filtered_tests,
        }

    @classmethod
    def _build_test_payload(
        cls, item: dict, section_key: str, include_structured_results: bool
    ) -> dict:
        clinical_interpretation = (item.get("clinical_interpretation") or "").strip()
        structured_results = item.get("structured_results") or {}

        payload = {
            "instrument_code": item.get("instrument_code"),
            "instrument_name": item.get("instrument_name") or item.get("instrument"),
            "clinical_interpretation": clinical_interpretation,
            "warnings": item.get("warnings") or [],
        }

        if not clinical_interpretation:
            payload["summary"] = item.get("summary") or ""

        should_include_structured = (
            include_structured_results and not clinical_interpretation
        )

        if (
            item.get("instrument_code") == "wisc4"
            and section_key in cls.WISC_SECTION_SUBTEST_CODES
        ):
            should_include_structured = True
            filtered_structured_results = cls._filter_wisc_structured_results(
                structured_results, section_key
            )
            payload["structured_results"] = filtered_structured_results
            payload["clinical_interpretation"] = ""
            payload["technical_basis"] = cls._build_wisc_domain_basis(
                filtered_structured_results, section_key
            )
        elif should_include_structured:
            payload["structured_results"] = structured_results

        if should_include_structured:
            payload["result_rows"] = item.get("result_rows") or []

        return payload

    @classmethod
    def _filter_wisc_structured_results(
        cls, structured_results: dict, section_key: str
    ) -> dict:
        allowed_codes = cls.WISC_SECTION_SUBTEST_CODES.get(section_key, set())
        if not structured_results or not allowed_codes:
            return structured_results or {}

        filtered_subtests = [
            subtest
            for subtest in (structured_results.get("subtestes") or [])
            if subtest.get("codigo") in allowed_codes
        ]
        filtered_indices = []
        for index in structured_results.get("indices") or []:
            index_subtests = [
                subtest
                for subtest in (index.get("subtestes") or [])
                if subtest.get("codigo") in allowed_codes
            ]
            if index_subtests:
                filtered_indices.append({**index, "subtestes": index_subtests})

        return {
            "confidence_level": structured_results.get("confidence_level"),
            "subtestes": filtered_subtests,
            "indices": filtered_indices,
        }

    @classmethod
    def _build_wisc_domain_basis(
        cls, structured_results: dict, section_key: str
    ) -> str:
        summary = cls.WISC_DOMAIN_SUMMARIES.get(section_key)
        subtests = structured_results.get("subtestes") or []
        if not summary:
            return ""
        if not subtests:
            return summary["intro"]

        low_labels = {
            "Dificuldade Leve",
            "Dificuldade Moderada",
            "Dificuldade Grave",
            "Média Inferior",
            "Limítrofe",
            "Inferior",
            "Extremamente Baixo",
        }
        low_count = sum(
            1 for item in subtests if item.get("classificacao") in low_labels
        )
        if low_count == 0:
            profile = summary["preserved"]
        elif low_count < len(subtests):
            profile = summary["mixed"]
        else:
            profile = summary["low"]

        lines = []
        for item in subtests:
            details = []
            if item.get("escore_padrao") is not None:
                details.append(f"escore padrão {item.get('escore_padrao')}")
            if item.get("percentil") is not None:
                details.append(f"percentil {item.get('percentil')}")
            suffix = f" ({', '.join(details)})" if details else ""
            lines.append(
                f"{item.get('subteste')}: {item.get('classificacao')}{suffix}."
            )

        return "\n\n".join(
            [
                summary["intro"],
                profile,
                "Subtestes relevantes do domínio: " + " ".join(lines),
            ]
        )

    @classmethod
    def _generator_config(cls, section_key: str) -> dict:
        config = cls.TEST_GENERATORS.get(section_key) or cls.SECTION_GENERATORS.get(
            section_key
        )
        if not config:
            raise ValueError(
                f"Configuracao de IA nao encontrada para a secao: {section_key}"
            )
        return config
