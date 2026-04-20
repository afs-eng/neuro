STANDARD_REFERENCE = (
    "CONSELHO FEDERAL DE PSICOLOGIA (CFP). Resolução do CRP nº 6, de 29 de "
    "março de 2019, e nº 31, de 2022. Institui o Manual de Elaboração de "
    "Documentos Escritos produzidos pelo psicólogo, decorrentes de avaliação "
    "psicológica; regras do registro documental elaborado pela(o) psicóloga(o), "
    "decorrentes da prestação de serviços psicológicos, diretrizes para a "
    "Avaliação Psicológica, o uso de métodos, técnicas e instrumentos reconhecidos "
    "cientificamente para uso na prática profissional, assim como o uso de "
    "procedimentos e recursos auxiliares. Brasília: CFP, 2019."
)


REFERENCE_BY_TEST_CODE = {
    "wisc4": "WECHSLER, D. WISC-IV – Escala de Inteligência Wechsler para Crianças – Quarta Edição. São Paulo: Pearson, 2013.",
    "wais3": "WECHSLER, D. WAIS-III – Escala de Inteligência Wechsler para Adultos – Terceira Edição. São Paulo: Casa do Psicólogo, 2004.",
    "wasi": "WECHSLER, D. WASI – Escala Wechsler Abreviada de Inteligência. São Paulo: Pearson, 2014.",
    "bpa2": "RUEDA, F. J. M. Bateria Psicológica para Avaliação da Atenção – BPA-2. São Paulo: Vetor Editora, 2013.",
    "fdt": "SALLES, J. F.; FONSECA, R. P.; PARENTE, M. A. M. P. Teste dos Cinco Dígitos (FDT). São Paulo: Casa do Psicólogo, 2011.",
    "ravlt": "SCHMIDT, M. Rey Auditory Verbal Learning Test: A Handbook. Los Angeles: Western Psychological Services, 1996.",
    "etdah_pais": "BENCZIK, E. B. P. Escala de Transtorno de Déficit de Atenção e Hiperatividade – E-TDAH (versão pais). São Paulo: Casa do Psicólogo, 2005.",
    "etdah_ad": "BENCZIK, E. B. P. Escala de Transtorno de Déficit de Atenção e Hiperatividade – E-TDAH (autorrelato). São Paulo: Casa do Psicólogo, 2005.",
    "scared": "BIRMAHER, B. et al. Screen for Child Anxiety Related Emotional Disorders (SCARED): Scale construction and psychometric characteristics. Journal of the American Academy of Child and Adolescent Psychiatry, v. 36, n. 4, p. 545-553, 1997.",
    "srs2": "CONSTANTINO, J. N.; GRUBER, C. P. SRS-2 – Social Responsiveness Scale, Second Edition: Manual. Torrance: Western Psychological Services, 2012.",
    "epq_j": "EYSENCK, H. J.; EYSENCK, S. B. G. Manual do Inventário de Personalidade de Eysenck – EPQ-J. São Paulo: Casa do Psicólogo, 1992.",
    "ebadep_a": "BAPTISTA, M. N. EBADEP-A – Escala Baptista de Depressão – Versão Adulto: Manual técnico. São Paulo: Vetor Editora.",
    "ebadep_ij": "BAPTISTA, M. N. EBADEP-IJ – Escala Baptista de Depressão (Versão Infantojuvenil): Manual técnico. São Paulo: Vetor Editora, s.d.",
    "ebaped_ij": "BAPTISTA, M. N. EBADEP-IJ – Escala Baptista de Depressão (Versão Infantojuvenil): Manual técnico. São Paulo: Vetor Editora, s.d.",
}


def build_references(validated_tests: list[dict]) -> list[str]:
    references = [STANDARD_REFERENCE]
    seen = {STANDARD_REFERENCE}

    for test in validated_tests or []:
        reference = REFERENCE_BY_TEST_CODE.get(test.get("instrument_code"))
        if reference and reference not in seen:
            references.append(reference)
            seen.add(reference)

    return references


def build_references_text(validated_tests: list[dict]) -> str:
    return "\n".join(build_references(validated_tests))
