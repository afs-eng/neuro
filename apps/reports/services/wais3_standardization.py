from __future__ import annotations


class WAIS3StandardizationService:
    SUPPORTED_SECTIONS = {
        "capacidade_cognitiva_global",
        "funcoes_executivas",
        "linguagem",
        "gnosias_praxias",
        "memoria_aprendizagem",
    }

    DOMAIN_SUBTESTS = {
        "funcoes_executivas": ["semelhancas", "compreensao", "raciocinio_matricial"],
        "linguagem": ["semelhancas", "vocabulario", "compreensao"],
        "gnosias_praxias": ["raciocinio_matricial", "cubos"],
        "memoria_aprendizagem": ["sequencia_numeros_letras", "digitos"],
    }

    DOMAIN_INTROS = {
        "funcoes_executivas": (
            "Interpretação e Observações Clínicas: A avaliação das funções executivas de {patient} foi realizada "
            "por meio dos subtestes Semelhanças, Compreensão e Raciocínio Matricial "
            "da Escala Wechsler de Inteligência para Adultos – Terceira Edição (WAIS-III). "
            "Esses subtestes permitem examinar habilidades de raciocínio abstrato, categorização "
            "conceitual, julgamento prático e resolução de problemas, domínios diretamente "
            "relacionados ao controle inibitório, flexibilidade cognitiva e planejamento."
        ),
        "linguagem": (
            "Interpretação e Observações Clínicas: A avaliação da linguagem de {patient} "
            "foi realizada por meio dos subtestes Semelhanças, Vocabulário e Compreensão "
            "da Escala Wechsler de Inteligência para Adultos – Terceira Edição (WAIS-III). "
            "Esses instrumentos permitem examinar habilidades de conceituação verbal, "
            "conhecimento lexical, formulação linguística, julgamento social e compreensão "
            "de normas."
        ),
        "gnosias_praxias": (
            "Interpretação e Observações Clínicas: A avaliação das habilidades visuoperceptivas e construtivas de "
            "{patient} foi realizada por meio dos subtestes Raciocínio Matricial e Cubos "
            "da Escala Wechsler de Inteligência para Adultos – Terceira Edição (WAIS-III). "
            "Esses subtestes investigam processos de percepção visual, integração "
            "visomotora, análise de padrões e organização espacial."
        ),
        "memoria_aprendizagem": (
            "Interpretação e Observações Clínicas: A avaliação da memória e aprendizagem de {patient} foi "
            "realizada por meio dos subtestes Sequência de Números e Letras e Dígitos "
            "da Escala Wechsler de Inteligência para Adultos – Terceira Edição (WAIS-III). "
            "Esses instrumentos examinam processos de memória operacional auditiva, atenção "
            "sustentada, manipulação de informações e capacidade de atualização cognitiva."
        ),
    }

    SUBTEST_SENTENCE_BUILDERS = {
        "semelhancas": lambda item: (
            "No subteste Semelhanças, o desempenho "
            f"situou-se na faixa {WAIS3StandardizationService._classification(item)}, "
            "sugerindo "
            f"{WAIS3StandardizationService._level_phrase(item, 'abstração verbal, formação de conceitos e estabelecimento de relações semânticas')}"
        ),
        "compreensao": lambda item: (
            "No subteste Compreensão, o desempenho "
            f"situou-se na faixa {WAIS3StandardizationService._classification(item)}, "
            "sugerindo "
            f"{WAIS3StandardizationService._level_phrase(item, 'julgamento prático, entendimento de normas sociais e resolução de situações do cotidiano')}"
        ),
        "raciocinio_matricial": lambda item: (
            "No subteste Raciocínio Matricial, o desempenho "
            f"situou-se na faixa {WAIS3StandardizationService._classification(item)}, "
            "indicando "
            f"{WAIS3StandardizationService._level_phrase(item, 'raciocínio lógico-abstrato não verbal, identificação de padrões, relações visuoespaciais e inferência visual')}"
        ),
        "vocabulario": lambda item: (
            "No subteste Vocabulário, o desempenho "
            f"situou-se na faixa {WAIS3StandardizationService._classification(item)}, "
            "sugerindo "
            f"{WAIS3StandardizationService._level_phrase(item, 'repertório lexical expressivo, precisão conceitual e definição verbal de palavras')}"
        ),
        "cubos": lambda item: (
            "No subteste Cubos, o desempenho "
            f"situou-se na faixa {WAIS3StandardizationService._classification(item)}, "
            "indicando "
            f"{WAIS3StandardizationService._level_phrase(item, 'praxias construtivas, organização visomotora, planejamento da ação e integração espacial')}"
        ),
        "sequencia_numeros_letras": lambda item: (
            "No subteste Sequência de Números e Letras, o resultado "
            f"situou-se na faixa {WAIS3StandardizationService._classification(item)}, "
            "sugerindo "
            f"{WAIS3StandardizationService._level_phrase(item, 'capacidade de reter, reorganizar e manipular informações auditivas em curto prazo')}"
        ),
        "digitos": lambda item: (
            "No subteste Dígitos, o desempenho "
            f"situou-se na faixa {WAIS3StandardizationService._classification(item)}, "
            "indicando "
            f"{WAIS3StandardizationService._level_phrase(item, 'atenção auditiva imediata, manutenção sequencial de informações verbais e sustentação atencional')}"
        ),
    }

    DOMAIN_CLOSINGS = {
        "funcoes_executivas": {
            "preserved": "Em análise clínica, a síntese dos achados sugere funcionamento executivo relativamente preservado, com recursos adequados para abstração, planejamento, flexibilidade cognitiva e resolução de problemas.",
            "mixed": "Em análise clínica, a síntese dos achados sugere perfil executivo heterogêneo, com recursos relativamente preservados em alguns componentes e fragilidades em outros, especialmente em tarefas de maior complexidade cognitiva.",
            "low": "Em análise clínica, a síntese dos achados sugere limitações importantes em abstração, planejamento, flexibilidade cognitiva e resolução de problemas, com potencial impacto sobre o desempenho funcional.",
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
        return section_key in cls.SUPPORTED_SECTIONS and cls._get_wais3_test(context) is not None

    @classmethod
    def build(cls, section_key: str, context: dict) -> str:
        test = cls._get_wais3_test(context)
        if not test:
            return ""

        if section_key == "capacidade_cognitiva_global":
            return cls._build_global_text(test, context)
        return cls._build_domain_text(section_key, test, context)

    @staticmethod
    def _get_wais3_test(context: dict) -> dict | None:
        for test in context.get("validated_tests") or []:
            if test.get("instrument_code") == "wais3":
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
        return test.get("structured_results") or test.get("classified_payload") or {}

    @classmethod
    def _build_global_text(cls, test: dict, context: dict) -> str:
        payload = cls._payload(test)
        indices = payload.get("indices") or {}
        
        qit = indices.get("qi_total") or {}
        qiv = indices.get("qi_verbal") or {}
        qie = indices.get("qi_execucao") or {}
        icv = indices.get("compreensao_verbal") or {}
        iop = indices.get("organizacao_perceptual") or {}
        imo = indices.get("memoria_operacional") or {}
        ivp = indices.get("velocidade_processamento") or {}
        gai = indices.get("gai") or {}
        
        qit_score = qit.get("pontuacao_composta")
        if qit_score is None:
            return (
                f"Capacidade Cognitiva Global: {cls._patient_label(context)} realizou o WAIS-III, instrumento "
                "destinado à avaliação do funcionamento intelectual global em adultos. No momento, as tabelas normativas "
                "de conversão de pontos brutos em escores ponderados ainda não estão preenchidas de forma suficiente "
                "para cálculo automatizado dos índices compostos, percentis e intervalos de confiança."
            )
        
        intro = (
            f"Capacidade Cognitiva Global: {cls._patient_label(context)} obteve, a partir da Escala Wechsler de "
            f"Inteligência para Adultos – Terceira Edição (WAIS-III), "
            f"Quociente de Inteligência Total (QIT = {qit_score}), classificado como {qit.get('classificacao', 'não informada')}. "
        )
        
        intro += "Em relação aos índices fatoriais, apresentou os seguintes resultados:"
        
        rows = []
        definitions = [
            ("Compreensão Verbal (ICV)", icv, "Conhecimento verbal e raciocínio verbal"),
            ("Organização Perceptual (IOP)", iop, "Raciocínio visual e integração espacial"),
            ("Memória Operacional (IMO)", imo, "Atenção e manipulação mental"),
            ("Velocidade de Processamento (IVP)", ivp, "Rapidez e eficiência visuomotora"),
            ("QI Verbal (QIV)", qiv, "Recursos verbais, compreensão e expressão"),
            ("QI de Execução (QIE)", qie, "Raciocínio não verbal e solução de problemas"),
        ]
        
        if gai.get("pontuacao_composta"):
            definitions.append(("Habilidade Geral (GAI)", gai, "Índice geral sem memória e velocidade"))
        
        for label, item, _ in definitions:
            score = item.get("pontuacao_composta")
            classification = item.get("classificacao")
            if score is not None:
                rows.append(f"- {label}: {score} — {classification or 'não classificado'}")
        
        closing = (
            f"Os resultados indicam funcionamento intelectual global situado na faixa {qit.get('classificacao', 'não definida')}, "
            "com análise detalhada dos domínios cognitivo-comportamentais apresentada nas seções seguintes."
        )
        
        parts = [intro] + rows + [closing]
        return "\n\n".join(parts)

    @classmethod
    def _build_domain_text(cls, section_key: str, test: dict, context: dict) -> str:
        payload = cls._payload(test)
        patient = cls._first_name(context)
        
        domain_subtests = cls.DOMAIN_SUBTESTS.get(section_key, [])
        if not domain_subtests:
            return ""
        
        subtests = payload.get("subtestes") or {}
        
        intro = cls.DOMAIN_INTROS.get(section_key, "").format(patient=patient)

        sentences = []
        for subtest_key in domain_subtests:
            if subtest_key in subtests:
                item = subtests[subtest_key] or {}
                builder = cls.SUBTEST_SENTENCE_BUILDERS.get(subtest_key)
                if builder:
                    sentences.append(builder(item))
        
        if not sentences:
            return intro + " Dados dos subtestes não disponíveis para análise."
        
        closing_key = "low"
        scores = []
        for subtest_key in domain_subtests:
            if subtest_key in subtests:
                item = subtests[subtest_key]
                if item and item.get("escore_ponderado"):
                    scores.append(item["escore_ponderado"])
        
        if scores:
            avg = sum(scores) / len(scores)
            if avg >= 8:
                closing_key = "preserved"
            elif avg >= 5:
                closing_key = "mixed"
        
        closing = cls.DOMAIN_CLOSINGS.get(section_key, {}).get(closing_key, "")

        extras = []
        if section_key == "linguagem":
            extras.append(
                "A fala espontânea deve ser interpretada em conjunto com a observação clínica direta, considerando fluência, articulação, ritmo, inteligibilidade, prosódia e funcionalidade comunicativa quando tais dados estiverem disponíveis."
            )
        elif section_key == "memoria_aprendizagem" and cls._has_test(context, "ravlt"):
            extras.append(
                "Os achados de memória operacional devem ser analisados em conjunto com o desempenho obtido no RAVLT, especialmente quanto à curva de aprendizagem, evocação tardia e reconhecimento."
            )

        parts = [intro] + sentences + extras + [closing]
        return "\n\n".join(parts)

    @staticmethod
    def _has_test(context: dict, instrument_code: str) -> bool:
        for test in context.get("validated_tests") or []:
            if test.get("instrument_code") == instrument_code:
                return True
        return False

    @staticmethod
    def _classification(item: dict) -> str:
        cls = item.get("classificacao")
        if cls:
            return cls
        raw = item.get("escore_ponderado") or item.get("pontuacao_composta")
        if raw is None:
            return "não disponível"
        if raw >= 12:
            return "Muito Superior"
        elif raw >= 10:
            return "Superior"
        elif raw >= 8:
            return "Média Superior"
        elif raw >= 6:
            return "Média"
        elif raw >= 4:
            return "Média Inferior"
        elif raw >= 2:
            return "Limítrofe"
        else:
            return "Extremamente Baixo"

    @staticmethod
    def _level_phrase(item: dict, abilities: str) -> str:
        raw = item.get("escore_ponderado") or item.get("pontuacao_composta")
        if raw is None:
            return "dados insuficientes para análise"
        
        if raw >= 12:
            return f"excelentes recursos em {abilities}"
        elif raw >= 10:
            return f"bons recursos em {abilities}"
        elif raw >= 8:
            return f"recursos acima da média em {abilities}"
        elif raw >= 6:
            return f"recursos médios em {abilities}"
        elif raw >= 4:
            return f"recursos abaixo da média em {abilities}"
        elif raw >= 2:
            return f"limitações em {abilities}"
        else:
            return f"comprometimento significativo em {abilities}"
