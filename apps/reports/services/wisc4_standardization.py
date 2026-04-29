from __future__ import annotations


class WISC4StandardizationService:
    SUPPORTED_SECTIONS = {
        "capacidade_cognitiva_global",
        "funcoes_executivas",
        "linguagem",
        "gnosias_praxias",
        "memoria_aprendizagem",
    }

    DOMAIN_SUBTESTS = {
        "funcoes_executivas": ["SM", "CN", "CO", "RM"],
        "linguagem": ["SM", "VC", "CO"],
        "gnosias_praxias": ["RM", "CB"],
        "memoria_aprendizagem": ["SNL", "DG"],
    }

    DOMAIN_INTROS = {
        "funcoes_executivas": (
            "Interpretação e Observações Clínicas: A avaliação das funções executivas de {patient} foi realizada "
            "por meio dos subtestes Semelhanças, Conceitos Figurativos, Compreensão e "
            "Raciocínio Matricial da Escala Wechsler de Inteligência para Crianças – "
            "Quarta Edição (WISC-IV). Esses subtestes permitem examinar habilidades de "
            "raciocínio abstrato, categorização conceitual, julgamento social e "
            "raciocínio lógico-visual, domínios diretamente relacionados à resolução de "
            "problemas, controle inibitório e flexibilidade cognitiva."
        ),
        "linguagem": (
            "Interpretação e Observações Clínicas: A avaliação da linguagem de {patient} "
            "foi realizada por meio dos subtestes Semelhanças, Vocabulário e Compreensão "
            "da Escala Wechsler de Inteligência para Crianças – Quarta Edição (WISC-IV). "
            "Esses instrumentos permitem examinar habilidades de conceituação verbal, "
            "conhecimento lexical, formulação linguística, julgamento social e compreensão "
            "de normas."
        ),
        "gnosias_praxias": (
            "Interpretação e Observações Clínicas: A avaliação das habilidades visuoperceptivas e construtivas de "
            "{patient} foi realizada por meio dos subtestes Raciocínio Matricial e Cubos "
            "da Escala Wechsler de Inteligência para Crianças – Quarta Edição (WISC-IV). "
            "Esses subtestes investigam processos de percepção visual, integração "
            "visomotora, análise de padrões e organização espacial."
        ),
        "memoria_aprendizagem": (
            "Interpretação e Observações Clínicas: A avaliação da memória e aprendizagem de {patient} foi "
            "realizada por meio dos subtestes Sequência de Números e Letras e Dígitos da "
            "Escala Wechsler de Inteligência para Crianças – Quarta Edição (WISC-IV). "
            "Esses instrumentos examinam processos de memória operacional auditiva, atenção "
            "sustentada, manipulação de informações e capacidade de atualização cognitiva."
        ),
    }

    SUBTEST_SENTENCE_BUILDERS = {
        "SM": lambda item: (
            "No subteste Semelhanças, o desempenho "
            f"situou-se na faixa {WISC4StandardizationService._classification(item)}, "
            "sugerindo "
            f"{WISC4StandardizationService._level_phrase(item, 'abstração verbal, formação de conceitos e estabelecimento de relações semânticas')}"
        ),
        "CN": lambda item: (
            "No subteste Conceitos Figurativos, o desempenho "
            f"situou-se na faixa {WISC4StandardizationService._classification(item)}, "
            "indicando "
            f"{WISC4StandardizationService._level_phrase(item, 'eficiência na formação de categorias não verbais, análise de atributos visuais e organização conceitual figurativa')}"
        ),
        "CO": lambda item: (
            "No subteste Compreensão, o desempenho "
            f"situou-se na faixa {WISC4StandardizationService._classification(item)}, "
            "sugerindo "
            f"{WISC4StandardizationService._level_phrase(item, 'julgamento prático, entendimento de normas sociais e resolução de situações do cotidiano')}"
        ),
        "RM": lambda item: (
            "No subteste Raciocínio Matricial, o desempenho "
            f"situou-se na faixa {WISC4StandardizationService._classification(item)}, "
            "indicando "
            f"{WISC4StandardizationService._level_phrase(item, 'raciocínio lógico-abstrato não verbal, identificação de padrões, relações visuoespaciais e inferência visual')}"
        ),
        "VC": lambda item: (
            "No subteste Vocabulário, o desempenho "
            f"situou-se na faixa {WISC4StandardizationService._classification(item)}, "
            "sugerindo "
            f"{WISC4StandardizationService._level_phrase(item, 'repertório lexical expressivo, precisão conceitual e definição verbal de palavras')}"
        ),
        "CB": lambda item: (
            "No subteste Cubos, o desempenho "
            f"situou-se na faixa {WISC4StandardizationService._classification(item)}, "
            "indicando "
            f"{WISC4StandardizationService._level_phrase(item, 'praxias construtivas, organização visomotora, planejamento da ação e integração espacial')}"
        ),
        "SNL": lambda item: (
            "No subteste Sequência de Números e Letras, o desempenho "
            f"situou-se na faixa {WISC4StandardizationService._classification(item)}, "
            "sugerindo "
            f"{WISC4StandardizationService._level_phrase(item, 'capacidade de reter, reorganizar e manipular informações auditivas em curto prazo')}"
        ),
        "DG": lambda item: (
            "No subteste Dígitos, o desempenho "
            f"situou-se na faixa {WISC4StandardizationService._classification(item)}, "
            "indicando "
            f"{WISC4StandardizationService._level_phrase(item, 'atenção auditiva imediata, manutenção sequencial de informações verbais e sustentação atencional')}"
        ),
    }

    DOMAIN_CLOSINGS = {
        "funcoes_executivas": {
            "preserved": "Em análise clínica, a síntese dos achados sugere funcionamento executivo relativamente preservado, com recursos adequados para abstração, planejamento, flexibilidade cognitiva e resolução de problemas.",
            "mixed": "Em análise clínica, a síntese dos achados sugere perfil executivo heterogêneo, com recursos relativamente preservados em alguns componentes e fragilidades em outros, especialmente em tarefas de maior complexidade cognitiva.",
            "low": "Em análise clínica, a síntese dos achados sugere limitações importantes em abstração, planejamento, flexibilidade cognitiva e resolução de problemas, com potencial impacto sobre o desempenho acadêmico e funcional.",
        },
        "linguagem": {
            "preserved": "Em análise clínica, a síntese dos achados sugere linguagem globalmente preservada, com recursos adequados para compreensão verbal, conceituação e comunicação funcional.",
            "mixed": "Em análise clínica, a síntese dos achados sugere perfil linguístico heterogêneo, com áreas preservadas e fragilidades pontuais em repertório lexical, abstração verbal ou uso funcional da linguagem.",
            "low": "Em análise clínica, a síntese dos achados sugere prejuízos relevantes no domínio da linguagem, com repercussões potenciais sobre compreensão verbal, repertório lexical e comunicação funcional.",
        },
        "gnosias_praxias": {
            "preserved": "Em análise clínica, a síntese dos achados sugere preservação das habilidades visuoperceptivas e construtivas, sem indícios relevantes de comprometimento nesse domínio.",
            "mixed": "Em análise clínica, a síntese dos achados sugere perfil visuoperceptivo e construtivo misto, com áreas relativamente preservadas coexistindo com fragilidades em organização espacial e praxia construtiva.",
            "low": "Em análise clínica, a síntese dos achados sugere comprometimento das habilidades visuoconstrutivas e perceptivas, com possível impacto em tarefas de cópia, construção, organização espacial e manipulação de estímulos visuais.",
        },
        "memoria_aprendizagem": {
            "preserved": "Em análise clínica, a síntese dos achados sugere preservação da memória operacional, com recursos adequados para retenção, manipulação mental de informações e seguimento de instruções.",
            "mixed": "Em análise clínica, a síntese dos achados sugere perfil mnésico heterogêneo, com oscilação entre recursos relativamente preservados e fragilidades em retenção ativa, manipulação mental ou sustentação atencional.",
            "low": "Em análise clínica, a síntese dos achados sugere prejuízo da memória operacional, com impacto sobre aprendizagem, seguimento de instruções, organização mental e processamento sequencial.",
        },
    }

    @classmethod
    def supports(cls, section_key: str, context: dict) -> bool:
        return section_key in cls.SUPPORTED_SECTIONS and cls._get_wisc4_test(context) is not None

    @classmethod
    def build(cls, section_key: str, context: dict) -> str:
        test = cls._get_wisc4_test(context)
        if not test:
            return ""

        if section_key == "capacidade_cognitiva_global":
            return cls._build_global_text(test, context)
        return cls._build_domain_text(section_key, test, context)

    @staticmethod
    def _get_wisc4_test(context: dict) -> dict | None:
        for test in context.get("validated_tests") or []:
            if test.get("instrument_code") == "wisc4":
                return test
        return None

    @staticmethod
    def _patient_label(context: dict) -> str:
        sex = (context.get("patient") or {}).get("sex")
        return "A paciente" if sex == "F" else "O paciente"

    @staticmethod
    def _first_name(context: dict) -> str:
        name = (context.get("patient") or {}).get("full_name") or "Paciente"
        return name.split(" ", 1)[0]

    @staticmethod
    def _payload(test: dict) -> dict:
        return test.get("structured_results") or {}

    @classmethod
    def _build_global_text(cls, test: dict, context: dict) -> str:
        payload = cls._payload(test)
        qit = payload.get("qit_data") or {}
        indices = {item.get("indice"): item for item in payload.get("indices") or []}
        intro = (
            f"Capacidade Cognitiva Global: a avaliação neuropsicológica de {cls._first_name(context)}, por meio da "
            "Escala Wechsler de Inteligência para Crianças – Quarta Edição (WISC-IV), possibilitou a análise do "
            "funcionamento intelectual global e dos principais domínios cognitivos. "
            f"{cls._first_name(context)} apresentou Quociente de Inteligência Total (QIT = {qit.get('escore_composto', 'não informado')}), "
            f"classificado como {qit.get('classificacao', 'não informada')}"
        )
        idade_cognitiva = payload.get("idade_cognitiva")
        if idade_cognitiva:
            intro += (
                f", com idade cognitiva estimada de {idade_cognitiva}"
            )
        intro += "."
        return "\n".join(
            [
                intro,
                "",
                cls._global_bullet(
                    "Compreensão Verbal",
                    "ICV",
                    indices.get("icv"),
                    "Avaliou o conhecimento verbal adquirido, o processo mental necessário para responder às questões formuladas, a capacidade de compreensão verbal e o raciocínio verbal.",
                ),
                cls._global_bullet(
                    "Organização Perceptual",
                    "IOP",
                    indices.get("iop"),
                    "Avaliou o raciocínio não verbal, a atenção para detalhes e a integração visomotora.",
                ),
                cls._global_bullet(
                    "Memória Operacional",
                    "IMO",
                    indices.get("imt"),
                    "Avaliou a atenção, a concentração e a memória operacional.",
                ),
                cls._global_bullet(
                    "Velocidade de Processamento",
                    "IVP",
                    indices.get("ivp"),
                    "Avaliou a capacidade de em realizar tarefas que demandam rapidez e precisão na análise de estímulos visuais.",
                ),
            ]
        )

    @staticmethod
    def _global_bullet(label: str, code: str, item: dict | None, description: str) -> str:
        item = item or {}
        return (
            f"- {label} ({code}) — {item.get('escore_composto', 'não informado')} — "
            f"{item.get('classificacao', 'não informada')} {description}"
        )

    @classmethod
    def _build_integrated_summary(cls, payload: dict) -> str:
        qit = payload.get("qit_data") or {}
        indices = {item.get("indice"): item for item in payload.get("indices") or []}
        paragraphs = []
        for code in ("icv", "iop", "imt", "ivp"):
            item = indices.get(code) or {}
            if not item.get("escore_composto"):
                continue
            paragraphs.append(
                cls._index_summary_sentence(
                    code,
                    item.get("escore_composto"),
                    item.get("classificacao") or "não informada",
                )
            )

        gai = payload.get("gai_data") or {}
        if gai.get("escore_composto"):
            paragraphs.append(
                f"O Índice de Habilidade Geral (GAI = {gai.get('escore_composto')}) foi classificado na faixa {gai.get('classificacao')}, representando uma estimativa do potencial global de raciocínio com menor influência da memória operacional e da velocidade de processamento."
            )
        cpi = payload.get("cpi_data") or {}
        if cpi.get("escore_composto"):
            paragraphs.append(
                f"O Índice de Proficiência Cognitiva (CPI = {cpi.get('escore_composto')}) foi classificado na faixa {cpi.get('classificacao')}, expressando a eficiência cognitiva operacional em tarefas com maior exigência de memória de trabalho e rapidez de processamento."
            )
        if gai.get("escore_composto") and cpi.get("escore_composto"):
            difference = int(gai.get("escore_composto") or 0) - int(cpi.get("escore_composto") or 0)
            if difference >= 8:
                paragraphs.append(
                    "A discrepância entre GAI e CPI sugere raciocínio global relativamente mais preservado do que a eficiência cognitiva operacional."
                )
            elif difference <= -8:
                paragraphs.append(
                    "A discrepância entre GAI e CPI sugere eficiência cognitiva operacional relativamente mais preservada do que o potencial global de raciocínio."
                )

        qit_class = qit.get("classificacao") or "não informada"
        if qit_class in {"Muito Superior", "Superior", "Média Superior", "Média"}:
            closing = (
                "Em síntese, o perfil cognitivo revela funcionamento intelectual global "
                "sem rebaixamento expressivo, devendo ser interpretado em conjunto com os "
                "demais domínios avaliados e com a funcionalidade observada no cotidiano."
            )
        elif qit_class == "Média Inferior":
            closing = (
                "Em síntese, o perfil cognitivo revela funcionamento intelectual global abaixo "
                "da média esperada, com potencial impacto sobre a aprendizagem, a organização "
                "do pensamento e o manejo de tarefas cognitivamente mais exigentes."
            )
        else:
            closing = (
                "Em síntese, o perfil cognitivo revela rebaixamento importante do funcionamento "
                "intelectual global, com repercussões potenciais sobre aprendizagem, autonomia, "
                "organização do comportamento e ritmo cognitivo."
            )
        paragraphs.append(closing)
        return "\n\n".join(paragraphs)

    @staticmethod
    def _index_summary_sentence(code: str, score: int, classification: str) -> str:
        labels = {
            "icv": "O Índice de Compreensão Verbal",
            "iop": "O Índice de Organização Perceptual",
            "imt": "O Índice de Memória Operacional",
            "ivp": "O Índice de Velocidade de Processamento",
        }
        domains = {
            "icv": "raciocínio verbal, abstração mediada pela linguagem e compreensão conceitual",
            "iop": "raciocínio não verbal, organização visuoespacial e integração perceptual",
            "imt": "atenção, retenção ativa e manipulação mental de informações",
            "ivp": "rapidez e eficiência no processamento de estímulos visuais simples",
        }
        return (
            f"{labels[code]} ({'IMO' if code == 'imt' else code.upper()} = {score}) foi classificado "
            f"na faixa {classification}, indicando desempenho em {domains[code]}."
        )

    @classmethod
    def _build_domain_text(cls, section_key: str, test: dict, context: dict) -> str:
        payload = cls._payload(test)
        subtests = {item.get("codigo"): item for item in payload.get("subtestes") or []}
        selected = [subtests.get(code) for code in cls.DOMAIN_SUBTESTS[section_key] if subtests.get(code)]
        patient = cls._first_name(context)
        parts = [cls.DOMAIN_INTROS[section_key].format(patient=patient)]

        detail_lines = []
        for item in selected:
            builder = cls.SUBTEST_SENTENCE_BUILDERS.get(item.get("codigo"))
            if builder:
                detail_lines.append(builder(item))
        if detail_lines:
            parts.extend(["", " ".join(detail_lines)])

        if section_key == "linguagem":
            parts.append(
                ""
            )
            parts.append(
                "A fala espontânea deve ser interpretada em conjunto com a observação clínica direta, considerando fluência, articulação, ritmo, inteligibilidade, prosódia e funcionalidade comunicativa quando tais dados estiverem disponíveis."
            )

        parts.extend(["", cls.DOMAIN_CLOSINGS[section_key][cls._domain_profile(selected)]])
        return "\n".join(parts)

    @staticmethod
    def _classification(item: dict) -> str:
        return item.get("classificacao") or "não informada"

    @staticmethod
    def _level_phrase(item: dict, domain: str) -> str:
        classification = item.get("classificacao") or ""
        if classification in {"Muito Superior", "Superior", "Média Superior", "Média"}:
            return f"recursos adequados para {domain}."
        if classification == "Média Inferior":
            return f"leve fragilidade em {domain}."
        return f"fragilidade importante em {domain}."

    @staticmethod
    def _domain_profile(subtests: list[dict]) -> str:
        if not subtests:
            return "mixed"
        low_labels = {
            "Média Inferior",
            "Limítrofe",
            "Inferior",
            "Extremamente Baixo",
            "Dificuldade Leve",
            "Dificuldade Moderada",
            "Dificuldade Grave",
        }
        low_count = sum(1 for item in subtests if item.get("classificacao") in low_labels)
        if low_count == 0:
            return "preserved"
        if low_count == len(subtests):
            return "low"
        return "mixed"
