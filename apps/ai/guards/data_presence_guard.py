class DataPresenceGuard:
    TEST_REQUIREMENTS = {
        "bpa2": {
            "codes": {"bpa2"},
            "message": "Nao ha resultados validados do BPA-2 suficientes para gerar esta secao com IA.",
        },
        "fdt": {
            "codes": {"fdt"},
            "message": "Nao ha resultados validados do FDT suficientes para gerar esta secao com IA.",
        },
        "ravlt": {
            "codes": {"ravlt"},
            "message": "Nao ha resultados validados do RAVLT suficientes para gerar esta secao com IA.",
        },
        "etdah_pais": {
            "codes": {"etdah_pais"},
            "message": "Nao ha resultados validados do E-TDAH-PAIS suficientes para gerar esta secao com IA.",
        },
        "etdah_ad": {
            "codes": {"etdah_ad"},
            "message": "Nao ha resultados validados do E-TDAH-AD suficientes para gerar esta secao com IA.",
        },
        "scared": {
            "codes": {"scared"},
            "message": "Nao ha resultados validados do SCARED suficientes para gerar esta secao com IA.",
        },
        "epq_j": {
            "codes": {"epq_j"},
            "message": "Nao ha resultados validados do EPQ-J suficientes para gerar esta secao com IA.",
        },
        "srs2": {
            "codes": {"srs2"},
            "message": "Nao ha resultados validados do SRS-2 suficientes para gerar esta secao com IA.",
        },
        "ebadep": {
            "codes": {"ebadep_a", "ebadep_ij", "ebaped_ij"},
            "message": "Nao ha resultados validados da EBADEP suficientes para gerar esta secao com IA.",
        },
    }
    SECTION_REQUIREMENTS = {
        "atencao": {
            "codes": {"bpa2", "etdah_ad", "etdah_pais"},
            "message": "Nao ha instrumentos atencionais validados suficientes para gerar esta secao com IA.",
        },
        "funcoes_executivas": {
            "codes": {"fdt", "wisc4", "wasi", "wais3"},
            "message": "Nao ha instrumentos executivos validados suficientes para gerar esta secao com IA.",
        },
        "linguagem": {
            "codes": {"wisc4", "wasi", "wais3"},
            "message": "Nao ha instrumentos de linguagem validados suficientes para gerar esta secao com IA.",
        },
        "gnosias_praxias": {
            "codes": {"wisc4", "wasi", "wais3"},
            "message": "Nao ha instrumentos visuoperceptivos validados suficientes para gerar esta secao com IA.",
        },
        "memoria_aprendizagem": {
            "codes": {"ravlt", "wisc4"},
            "message": "Nao ha instrumentos de memoria e aprendizagem validados suficientes para gerar esta secao com IA.",
        },
        "capacidade_cognitiva_global": {
            "codes": {"wisc4", "wasi", "wais3"},
            "message": "Nao ha instrumentos cognitivos globais validados suficientes para gerar esta secao com IA.",
        },
        "aspectos_emocionais_comportamentais": {
            "codes": {
                "scared",
                "srs2",
                "epq_j",
                "ebadep_a",
                "ebadep_ij",
                "ebaped_ij",
            },
            "message": "Nao ha escalas emocionais e comportamentais validadas suficientes para gerar esta secao com IA.",
        },
    }

    @classmethod
    def validate_section_context(cls, section_key: str, context: dict) -> list[str]:
        warnings: list[str] = []
        tests = context.get("validated_tests") or []
        requirement = cls.TEST_REQUIREMENTS.get(
            section_key
        ) or cls.SECTION_REQUIREMENTS.get(section_key)
        if not requirement:
            return warnings

        has_required_data = any(
            item.get("instrument_code") in requirement["codes"] for item in tests
        )
        if not has_required_data:
            warnings.append(requirement["message"])
        return warnings
