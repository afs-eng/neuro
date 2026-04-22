SECTION_REGISTRY: dict[str, dict] = {
    "identificacao": {
        "title": "1. Identificação",
        "order": 1,
        "required_any_codes": (),
    },
    "descricao_demanda": {
        "title": "2. Descrição da Demanda",
        "order": 2,
        "required_any_codes": (),
    },
    "procedimentos": {
        "title": "3. Procedimentos",
        "order": 3,
        "required_any_codes": (),
    },
    "historia_pessoal": {
        "title": "4. História Pessoal",
        "order": 4,
        "required_any_codes": (),
    },
    "capacidade_cognitiva_global": {
        "title": "5. Capacidade Cognitiva Global",
        "order": 5,
        "supports_ai": True,
        "prompt_name": "reports/capacidade_cognitiva_global_prompt.txt",
        "codes": {"wisc4", "wasi", "wais3"},
        "kind": "section",
        "timeout": 1800,
        "required_any_codes": (),
        "validation": {
            "required_any_codes": {"wisc4", "wasi", "wais3"},
            "message": "Nao ha instrumentos cognitivos globais validados suficientes para gerar esta secao com IA.",
        },
    },
    "funcoes_executivas": {
        "title": "6. Funções Executivas",
        "order": 6,
        "supports_ai": True,
        "prompt_name": "reports/funcoes_executivas_prompt.txt",
        "codes": {"fdt", "wisc4", "wasi", "wais3"},
        "kind": "section",
        "timeout": 1800,
        "required_any_codes": {"fdt", "wisc4"},
        "validation": {
            "required_any_codes": {"fdt", "wisc4", "wasi", "wais3"},
            "message": "Nao ha instrumentos executivos validados suficientes para gerar esta secao com IA.",
        },
    },
    "linguagem": {
        "title": "7. Linguagem",
        "order": 7,
        "supports_ai": True,
        "prompt_name": "reports/linguagem_prompt.txt",
        "codes": {"wisc4", "wasi", "wais3"},
        "kind": "section",
        "timeout": 1800,
        "required_any_codes": {"wisc4", "wasi", "wais3"},
        "validation": {
            "required_any_codes": {"wisc4", "wasi", "wais3"},
            "message": "Nao ha instrumentos de linguagem validados suficientes para gerar esta secao com IA.",
        },
    },
    "gnosias_praxias": {
        "title": "8. Gnosias e Praxias",
        "order": 8,
        "supports_ai": True,
        "prompt_name": "reports/gnosias_praxias_prompt.txt",
        "codes": {"wisc4", "wasi", "wais3"},
        "kind": "section",
        "timeout": 1800,
        "required_any_codes": {"wisc4", "wasi", "wais3"},
        "validation": {
            "required_any_codes": {"wisc4", "wasi", "wais3"},
            "message": "Nao ha instrumentos visuoperceptivos validados suficientes para gerar esta secao com IA.",
        },
    },
    "memoria_aprendizagem": {
        "title": "9. Memória e Aprendizagem",
        "order": 9,
        "supports_ai": True,
        "prompt_name": "reports/memoria_aprendizagem_prompt.txt",
        "codes": {"ravlt", "wisc4"},
        "kind": "section",
        "timeout": 1800,
        "required_any_codes": {"ravlt", "wisc4"},
        "validation": {
            "required_any_codes": {"ravlt", "wisc4"},
            "message": "Nao ha instrumentos de memoria e aprendizagem validados suficientes para gerar esta secao com IA.",
        },
    },
    "bpa2": {
        "title": "10. BPA-2",
        "order": 10,
        "supports_ai": True,
        "prompt_name": "reports/bpa2_prompt.txt",
        "codes": {"bpa2"},
        "kind": "test",
        "timeout": 1200,
        "required_any_codes": {"bpa2"},
        "validation": {
            "required_any_codes": {"bpa2"},
            "message": "Nao ha resultados validados do BPA-2 suficientes para gerar esta secao com IA.",
        },
    },
    "ravlt": {
        "title": "11. RAVLT",
        "order": 11,
        "supports_ai": True,
        "prompt_name": "reports/ravlt_prompt.txt",
        "codes": {"ravlt"},
        "kind": "test",
        "timeout": 1200,
        "required_any_codes": {"ravlt"},
        "validation": {
            "required_any_codes": {"ravlt"},
            "message": "Nao ha resultados validados do RAVLT suficientes para gerar esta secao com IA.",
        },
    },
    "fdt": {
        "title": "12. FDT",
        "order": 12,
        "supports_ai": True,
        "prompt_name": "reports/fdt_prompt.txt",
        "codes": {"fdt"},
        "kind": "test",
        "timeout": 1200,
        "required_any_codes": {"fdt"},
        "validation": {
            "required_any_codes": {"fdt"},
            "message": "Nao ha resultados validados do FDT suficientes para gerar esta secao com IA.",
        },
    },
    "etdah_pais": {
        "title": "13. E-TDAH-PAIS",
        "order": 13,
        "supports_ai": True,
        "prompt_name": "reports/etdah_pais_prompt.txt",
        "codes": {"etdah_pais"},
        "kind": "test",
        "timeout": 1500,
        "required_any_codes": {"etdah_pais"},
        "validation": {
            "required_any_codes": {"etdah_pais"},
            "message": "Nao ha resultados validados do E-TDAH-PAIS suficientes para gerar esta secao com IA.",
        },
    },
    "etdah_ad": {
        "title": "14. E-TDAH-AD",
        "order": 14,
        "supports_ai": True,
        "prompt_name": "reports/etdah_ad_prompt.txt",
        "codes": {"etdah_ad"},
        "kind": "test",
        "timeout": 1500,
        "required_any_codes": {"etdah_ad"},
        "validation": {
            "required_any_codes": {"etdah_ad"},
            "message": "Nao ha resultados validados do E-TDAH-AD suficientes para gerar esta secao com IA.",
        },
    },
    "scared": {
        "title": "15. SCARED",
        "order": 15,
        "supports_ai": True,
        "prompt_name": "reports/scared_prompt.txt",
        "codes": {"scared"},
        "kind": "test",
        "timeout": 1500,
        "required_any_codes": {"scared"},
        "validation": {
            "required_any_codes": {"scared"},
            "message": "Nao ha resultados validados do SCARED suficientes para gerar esta secao com IA.",
        },
    },
    "epq_j": {
        "title": "16. EPQ-J",
        "order": 16,
        "supports_ai": True,
        "prompt_name": "reports/epq_j_prompt.txt",
        "codes": {"epq_j"},
        "kind": "test",
        "timeout": 1500,
        "required_any_codes": {"epq_j"},
        "validation": {
            "required_any_codes": {"epq_j"},
            "message": "Nao ha resultados validados do EPQ-J suficientes para gerar esta secao com IA.",
        },
    },
    "srs2": {
        "title": "17. SRS-2",
        "order": 17,
        "supports_ai": True,
        "prompt_name": "reports/srs2_prompt.txt",
        "codes": {"srs2"},
        "kind": "test",
        "timeout": 1500,
        "required_any_codes": {"srs2"},
        "validation": {
            "required_any_codes": {"srs2"},
            "message": "Nao ha resultados validados do SRS-2 suficientes para gerar esta secao com IA.",
        },
    },
    "ebadep": {
        "title": "18. EBADEP",
        "order": 18,
        "supports_ai": True,
        "prompt_name": "reports/ebadep_prompt.txt",
        "codes": {"ebadep_a", "ebadep_ij", "ebaped_ij"},
        "kind": "test",
        "timeout": 1800,
        "required_any_codes": {"ebadep_a", "ebadep_ij", "ebaped_ij"},
        "validation": {
            "required_any_codes": {"ebadep_a", "ebadep_ij", "ebaped_ij"},
            "message": "Nao ha resultados validados da EBADEP suficientes para gerar esta secao com IA.",
        },
    },
    "referencias_bibliograficas": {
        "title": "23. Referências Bibliográficas",
        "order": 23,
        "required_any_codes": (),
    },
    "aspectos_emocionais_comportamentais": {
        "title": "19. Aspectos Emocionais, Comportamentais e Escalas Complementares",
        "order": 19,
        "supports_ai": True,
        "prompt_name": "reports/aspectos_emocionais_comportamentais_prompt.txt",
        "codes": {
            "scared",
            "srs2",
            "epq_j",
            "ebadep_a",
            "ebadep_ij",
            "ebaped_ij",
        },
        "kind": "section",
        "timeout": 2400,
        "required_any_codes": {
            "scared",
            "srs2",
            "epq_j",
            "ebadep_a",
            "ebadep_ij",
            "ebaped_ij",
        },
        "enable_when_adolescent": True,
        "validation": {
            "required_any_codes": {
                "scared",
                "srs2",
                "epq_j",
                "ebadep_a",
                "ebadep_ij",
                "ebaped_ij",
            },
            "message": "Nao ha escalas emocionais e comportamentais validadas suficientes para gerar esta secao com IA.",
        },
    },
    "conclusao": {
        "title": "20. Conclusão",
        "order": 20,
        "supports_ai": True,
        "prompt_name": "reports/conclusao_prompt.txt",
        "kind": "section",
        "timeout": 2400,
        "required_any_codes": (),
    },
    "hipotese_diagnostica": {
        "title": "21. Hipótese Diagnóstica",
        "order": 21,
        "required_any_codes": (),
    },
    "sugestoes_conduta": {
        "title": "22. Sugestões de Conduta",
        "order": 22,
        "required_any_codes": (),
    },
}


def get_section_config(section_key: str) -> dict:
    config = SECTION_REGISTRY.get(section_key)
    if not config:
        raise ValueError(f"Configuracao nao encontrada para a secao: {section_key}")
    return config


def get_ai_section_config(section_key: str) -> dict:
    config = get_section_config(section_key)
    if not config.get("supports_ai"):
        raise ValueError(
            f"Configuracao de IA nao encontrada para a secao: {section_key}"
        )
    return config


def get_section_validation(section_key: str) -> dict:
    return get_section_config(section_key).get("validation") or {}


def list_section_configs() -> list[tuple[str, dict]]:
    return sorted(SECTION_REGISTRY.items(), key=lambda item: item[1].get("order", 0))
