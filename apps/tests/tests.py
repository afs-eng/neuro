from django.test import SimpleTestCase

from apps.tests.bai import BAIModule
from apps.tests.base.types import TestContext
from apps.tests.cars2_hf import CARS2HFModule
from apps.tests.cars2_hf.classifiers import classify_cars2_hf
from apps.tests.cars2_hf.loaders import load_cars2_hf_norms
from apps.tests.etdah_ad import ETDAHADModule
from apps.tests.etdah_pais import ETDAHPAISModule
from apps.tests.epq_j import EPQJModule
from apps.tests.fdt import FDTModule
from apps.tests.mchat import MCHATModule
from apps.tests.mchat.constants import FAILURE_RULES, ITEMS
from apps.tests.ravlt import RAVLTModule
from apps.tests.norms.bai import get_norms_metadata, lookup_t_score
from apps.tests.scared import SCAREDModule
from apps.tests.srs2 import SRS2Module
from apps.tests.srs2.norms import get_norm_data


class BAINormsTests(SimpleTestCase):
    def test_lookup_t_score_uses_official_ranges(self):
        self.assertEqual(lookup_t_score(0), 39)
        self.assertEqual(lookup_t_score(3), 42)
        self.assertEqual(lookup_t_score(4), 42)
        self.assertEqual(lookup_t_score(47), 79)
        self.assertEqual(lookup_t_score(63), 80)

    def test_norms_metadata_exposes_expected_fields(self):
        metadata = get_norms_metadata()

        self.assertEqual(metadata["instrument"], "BAI")
        self.assertEqual(metadata["scale"], "Amostra Geral (T)")
        self.assertEqual(metadata["dimension"], "Escore Total")
        self.assertEqual(metadata["age_range"], "18-90")
        self.assertEqual(metadata["fidedignidade"], 0.90)
        self.assertEqual(metadata["reliability"], 0.90)


class BAIModuleTests(SimpleTestCase):
    def test_classify_returns_compatible_classification_shape(self):
        module = BAIModule()
        context = TestContext(
            patient_name="Paciente Teste",
            evaluation_id=1,
            instrument_code="bai",
            raw_scores={f"item_{index:02d}": 1 for index in range(1, 22)},
        )

        computed = module.compute(context)
        classified = module.classify(computed)

        self.assertEqual(classified["escore_total"], 21)
        self.assertEqual(classified["faixa_normativa"], "Moderado")
        self.assertEqual(classified["classificacao"]["label"], "Moderado")
        self.assertEqual(classified["classificacao"]["raw"]["label"], "Moderado")
        self.assertEqual(classified["classificacao_raw"]["label"], "Moderado")


class CARS2HFModuleTests(SimpleTestCase):
    def test_loads_norms_and_classifies_example_payload(self):
        norms = load_cars2_hf_norms()
        self.assertGreater(len(norms), 0)

        module = CARS2HFModule()
        context = TestContext(
            patient_name="Paciente Exemplo",
            evaluation_id=1,
            instrument_code="CARS2_HF",
            raw_scores={
                "patient_name": "Paciente Exemplo",
                "evaluation_date": "2026-04-15",
                "examiner_name": "Andre",
                "birth_date": "2016-02-10",
                "age_years": 10,
                "age_months": 2,
                "informant": "Mae",
                "items": {
                    "compreensao_socio_emocional": {
                        "score": 2.5,
                        "observations": "Dificuldade para compreender nuances emocionais.",
                    },
                    "expressao_emocional_regulacao": {
                        "score": 2.0,
                        "observations": "Oscilacoes emocionais e rigidez em situacoes frustrantes.",
                    },
                    "relacionamento_com_pessoas": {
                        "score": 3.0,
                        "observations": "Baixa reciprocidade social.",
                    },
                    "uso_do_corpo": {
                        "score": 1.5,
                        "observations": "Sem estereotipias evidentes; leve rigidez motora.",
                    },
                    "uso_objetos_brincadeiras": {
                        "score": 2.5,
                        "observations": "Brincadeira simbolica restrita.",
                    },
                    "adaptacao_mudancas_interesses_restritos": {
                        "score": 3.0,
                        "observations": "Resistencia importante a mudancas.",
                    },
                    "resposta_visual": {
                        "score": 2.5,
                        "observations": "Contato visual inconsistente.",
                    },
                    "resposta_auditiva": {
                        "score": 1.5,
                        "observations": "Responde ao nome, mas de forma irregular.",
                    },
                    "resposta_sensorial": {
                        "score": 2.0,
                        "observations": "Sensibilidade seletiva a texturas.",
                    },
                    "medo_ou_ansiedade": {
                        "score": 2.0,
                        "observations": "Ansiedade em situacoes novas.",
                    },
                    "comunicacao_verbal": {
                        "score": 2.5,
                        "observations": "Discurso pouco reciproco.",
                    },
                    "comunicacao_nao_verbal": {
                        "score": 3.0,
                        "observations": "Gestos pouco integrados a comunicacao.",
                    },
                    "integracao_pensamento_cognicao": {
                        "score": 2.0,
                        "observations": "Dificuldade em integrar informacoes globais.",
                    },
                    "resposta_intelectual": {
                        "score": 1.5,
                        "observations": "Funcionamento cognitivo global preservado, com discrepancias.",
                    },
                    "impressoes_gerais": {
                        "score": 3.0,
                        "observations": "Conjunto clinico compativel com alteracoes do espectro autista.",
                    },
                },
            },
        )

        self.assertEqual(module.validate(context), [])

        computed = module.compute(context)
        self.assertEqual(computed["raw_total"], 34.0)
        self.assertEqual(computed["t_score"], 51)
        self.assertEqual(computed["percentile"], "54")

        classified = module.classify(computed)
        self.assertEqual(classified["severity_code"], "severe")
        self.assertEqual(classify_cars2_hf(34.0)["severity_code"], "severe")

        interpretation = module.interpret(context, {**computed, **classified})
        self.assertIn("CARS2-HF evidenciou escore bruto total de 34.0", interpretation)
        self.assertIn("Relacionamento com pessoas", interpretation)


class MCHATModuleTests(SimpleTestCase):
    def test_computes_failures_and_positive_triage(self):
        module = MCHATModule()
        items = {
            slug: {
                "answer": FAILURE_RULES[number]
                if number in {1, 2, 7}
                else ("Não" if FAILURE_RULES[number] == "Sim" else "Sim")
            }
            for number, slug in ITEMS
        }

        context = TestContext(
            patient_name="Paciente M-CHAT",
            evaluation_id=1,
            instrument_code="MCHAT",
            raw_scores={
                "patient_name": "Paciente M-CHAT",
                "evaluation_date": "2026-04-15",
                "birth_date": "2024-02-10",
                "age_months": 22,
                "respondent_name": "Mae",
                "respondent_relationship": "Mãe",
                "items": items,
            },
        )

        self.assertEqual(module.validate(context), [])

        computed = module.compute(context)
        self.assertEqual(computed["critical_failures"], 2)
        self.assertEqual(computed["total_failures"], 3)

        classified = module.classify(computed)
        self.assertEqual(classified["screen_code"], "positive")

        interpretation = module.interpret(context, {**computed, **classified})
        self.assertIn("Triagem positiva", interpretation)
        self.assertIn("itens críticos", interpretation)


class FDTModuleTests(SimpleTestCase):
    def test_compute_exposes_dynamic_chart_payload(self):
        module = FDTModule()
        context = TestContext(
            patient_name="Larissa Souza",
            evaluation_id=1,
            instrument_code="fdt",
            raw_scores={
                "leitura": {"tempo": 18, "erros": 0},
                "contagem": {"tempo": 22, "erros": 1},
                "escolha": {"tempo": 26, "erros": 2},
                "alternancia": {"tempo": 35, "erros": 3},
            },
            reviewed_scores={"age": 9},
        )

        computed = module.compute(context)

        automaticos = computed["charts"]["automaticos"]
        controlados = computed["charts"]["controlados"]

        self.assertEqual(automaticos["categories"][0], "Sem Indicativo de Déficit")
        self.assertEqual(automaticos["series"][0]["label"], "CONTAGEM")
        self.assertEqual(automaticos["series"][0]["values"][4], 1)
        self.assertEqual(automaticos["series"][1]["values"][5], 18.0)
        self.assertEqual(controlados["series"][0]["label"], "FLEXIBILIDADE")
        self.assertEqual(controlados["series"][0]["values"][4], 0)
        self.assertEqual(controlados["series"][2]["values"][4], 3)

    def test_interpretation_for_preserved_profile_mentions_absence_of_errors(self):
        module = FDTModule()
        context = TestContext(
            patient_name="Larissa Souza",
            evaluation_id=1,
            instrument_code="fdt",
        )
        merged_data = {
            "metric_results": [
                {"codigo": "leitura", "classificacao": "Media", "categoria": "Processos Automaticos"},
                {"codigo": "contagem", "classificacao": "Superior", "categoria": "Processos Automaticos"},
                {"codigo": "escolha", "classificacao": "Media", "categoria": "Processos Controlados"},
                {"codigo": "alternancia", "classificacao": "Media Superior", "categoria": "Processos Controlados"},
                {"codigo": "inibicao", "classificacao": "Media", "categoria": "Processos Controlados"},
                {"codigo": "flexibilidade", "classificacao": "Superior", "categoria": "Processos Controlados"},
            ],
            "erros": {
                "leitura": {"qtde_erros": 0},
                "contagem": {"qtde_erros": 0},
                "escolha": {"qtde_erros": 0},
                "alternancia": {"qtde_erros": 0},
            },
        }

        interpretation = module.interpret(context, merged_data)

        self.assertIn("Larissa", interpretation)
        self.assertIn("A ausência de erros em todas as etapas", interpretation)
        self.assertIn("Em análise clínica", interpretation)

    def test_interpretation_for_altered_profile_mentions_controlled_errors(self):
        module = FDTModule()
        context = TestContext(
            patient_name="Bruno Lima",
            evaluation_id=1,
            instrument_code="fdt",
        )
        merged_data = {
            "metric_results": [
                {"codigo": "leitura", "classificacao": "Media", "categoria": "Processos Automaticos"},
                {"codigo": "contagem", "classificacao": "Media Inferior", "categoria": "Processos Automaticos"},
                {"codigo": "escolha", "classificacao": "Inferior", "categoria": "Processos Controlados"},
                {"codigo": "alternancia", "classificacao": "Muito Inferior", "categoria": "Processos Controlados"},
                {"codigo": "inibicao", "classificacao": "Inferior", "categoria": "Processos Controlados"},
                {"codigo": "flexibilidade", "classificacao": "Media", "categoria": "Processos Controlados"},
            ],
            "erros": {
                "leitura": {"qtde_erros": 0},
                "contagem": {"qtde_erros": 1},
                "escolha": {"qtde_erros": 3},
                "alternancia": {"qtde_erros": 4},
            },
        }

        interpretation = module.interpret(context, merged_data)

        self.assertIn("A frequência elevada de erros", interpretation)
        self.assertIn("controle inibitório", interpretation)
        self.assertIn("Em análise clínica", interpretation)


class RAVLTModuleTests(SimpleTestCase):
    def test_classify_exposes_dynamic_chart_payload(self):
        module = RAVLTModule()
        context = TestContext(
            patient_name="Ana Souza",
            evaluation_id=1,
            instrument_code="ravlt",
            raw_scores={
                "a1": 7,
                "a2": 8,
                "a3": 12,
                "a4": 13,
                "a5": 13,
                "b": 5,
                "a6": 12,
                "a7": 11,
                "reconhecimento": 14,
            },
        )

        computed = module.compute(context)
        classified = module.classify(computed, idade=21)

        chart = classified["chart"]
        self.assertEqual(chart["labels"][0], "A1")
        self.assertEqual(chart["labels"][-1], "I.R.")
        self.assertEqual(chart["series"][0]["label"], "Esperado")
        self.assertEqual(chart["series"][1]["label"], "Mínimo")
        self.assertEqual(chart["series"][2]["label"], "Obtido")
        self.assertEqual(chart["series"][2]["values"][:4], [7.0, 8.0, 12.0, 13.0])
        self.assertEqual(chart["series"][2]["values"][8], -21.0)


class ETDAHPAISModuleTests(SimpleTestCase):
    def test_non_clinical_classifications_are_not_treated_as_deficit(self):
        module = ETDAHPAISModule()
        context = TestContext(
            patient_name="Debora Silva",
            evaluation_id=1,
            instrument_code="etdah_pais",
            raw_scores={
                "age": 10,
                "sex": "F",
                "responses": {},
            },
        )
        merged_data = {
            "raw_scores": {
                "fator_1": 40,
                "fator_2": 35,
                "fator_3": 45,
                "fator_4": 24,
                "escore_geral": 150,
            },
            "age": 10,
            "sex": "F",
        }

        interpretation = module.interpret(context, merged_data)

        self.assertIn("Fator 1 — Regulação Emocional", interpretation)
        self.assertIn("funcionamento dentro dos limites esperados", interpretation)
        self.assertEqual(interpretation.count("Em análise clínica"), 1)

    def test_focal_elevation_is_described_without_automatic_diagnostic_hypothesis(self):
        module = ETDAHPAISModule()
        context = TestContext(
            patient_name="Debora Silva",
            evaluation_id=1,
            instrument_code="etdah_pais",
            raw_scores={
                "age": 10,
                "sex": "F",
                "responses": {},
            },
        )
        merged_data = {
            "raw_scores": {
                "fator_1": 40,
                "fator_2": 70,
                "fator_3": 45,
                "fator_4": 45,
                "escore_geral": 150,
            },
            "age": 10,
            "sex": "F",
        }

        interpretation = module.interpret(context, merged_data)

        self.assertIn("Fator 2 — Hiperatividade/Impulsividade", interpretation)
        self.assertIn("Fator 4 — Atenção", interpretation)
        self.assertIn("sem configuração de comprometimento global amplo", interpretation)
        self.assertIn("Há hipótese diagnóstica de Transtorno do Déficit de Atenção e Hiperatividade, apresentação combinada", interpretation)


class ETDAHADModuleTests(SimpleTestCase):
    def test_non_clinical_classifications_are_not_treated_as_deficit(self):
        module = ETDAHADModule()
        context = TestContext(
            patient_name="Marina Costa",
            evaluation_id=1,
            instrument_code="etdah_ad",
            raw_scores={
                "schooling": "higher",
                "responses": {},
            },
        )
        merged_data = {
            "raw_scores": {
                "D": 30,
                "I": 30,
                "AE": 4,
                "AAMA": 18,
                "H": 10,
            },
            "schooling": "higher",
        }

        interpretation = module.interpret(context, merged_data)

        self.assertIn("Fator 1 — Desatenção", interpretation)
        self.assertIn("funcionamento dentro dos limites esperados", interpretation)
        self.assertEqual(interpretation.count("Em análise integrada"), 1)

    def test_elevated_domains_are_summarized_without_automatic_diagnostic_hypothesis(self):
        module = ETDAHADModule()
        context = TestContext(
            patient_name="Marina Costa",
            evaluation_id=1,
            instrument_code="etdah_ad",
            raw_scores={
                "schooling": "higher",
                "responses": {},
            },
        )
        merged_data = {
            "raw_scores": {
                "D": 60,
                "I": 55,
                "AE": 10,
                "AAMA": 25,
                "H": 18,
            },
            "schooling": "higher",
        }

        interpretation = module.interpret(context, merged_data)

        self.assertIn("Fator 1 — Desatenção", interpretation)
        self.assertIn("Fator 4 — Autorregulação da Atenção, Motivação e Ação", interpretation)
        self.assertIn("Em análise integrada", interpretation)
        self.assertIn("há hipótese diagnóstica de Transtorno do Déficit de Atenção e Hiperatividade (TDAH), apresentação combinada", interpretation)


class SRS2ModuleTests(SimpleTestCase):
    def test_female_school_age_norms_are_available(self):
        self.assertEqual(get_norm_data(17, "idade_escolar", "F", "percepcao_social"), (78.0, 99.0))
        self.assertEqual(get_norm_data(54, "idade_escolar", "F", "cis"), (61.0, 87.0))
        self.assertEqual(get_norm_data(80, "idade_escolar", "F", "total"), (65.0, 93.0))

    def test_classify_uses_female_school_age_norms(self):
        module = SRS2Module()
        computed = {
            "form": "idade_escolar",
            "percepcao_social": {"nome": "Percepção Social", "escore": 17, "max": 21},
            "cognicao_social": {"nome": "Cognição Social", "escore": 26, "max": 24},
            "comunicacao_social": {"nome": "Comunicação Social", "escore": 49, "max": 33},
            "motivacao_social": {"nome": "Motivação Social", "escore": 28, "max": 33},
            "padroes_restritos": {"nome": "Padrões Restritos e Repetitivos", "escore": 31, "max": 24},
            "cis": {"nome": "Comunicação e Interação Social", "escore": 54, "max": 111},
            "total": {"nome": "Pontuação SRS-2 Total", "escore": 80, "max": 195},
        }

        classified = module.classify(computed, gender="F", age=10)

        self.assertEqual(classified["faixa_etaria"], "6 a 18 anos")
        self.assertEqual(classified["resultados"][0]["tscore"], 78.0)
        self.assertEqual(classified["resultados"][0]["percentil"], 99.0)
        self.assertEqual(classified["resultados"][0]["classificacao"], "Grave")


class SCAREDModuleTests(SimpleTestCase):
    def test_autorrelato_classification_uses_norms(self):
        module = SCAREDModule()
        context = TestContext(
            patient_name="Paciente SCARED",
            evaluation_id=1,
            instrument_code="scared",
            patient_age=10,
            raw_scores={
                "form": "child",
                "gender": "F",
                "age": 10,
                "responses": {str(i): 2 for i in range(1, 42)},
            },
        )

        self.assertEqual(module.validate(context), [])

        computed = module.compute(context)
        classified = module.classify(computed, idade=10)
        interpretation = module.interpret(context, classified)

        self.assertEqual(classified["form_type"], "child")
        self.assertEqual(classified["sexo"], "feminino")
        self.assertTrue(any(item.get("percentil") is not None for item in classified["analise_geral"]))
        self.assertIn("SCARED - Autorrelato", interpretation)

    def test_parent_classification_uses_cutoffs(self):
        module = SCAREDModule()
        context = TestContext(
            patient_name="Paciente SCARED",
            evaluation_id=1,
            instrument_code="scared",
            patient_age=10,
            raw_scores={
                "form": "parent",
                "gender": "M",
                "age": 10,
                "responses": {str(i): 2 for i in range(1, 42)},
            },
        )

        self.assertEqual(module.validate(context), [])

        computed = module.compute(context)
        classified = module.classify(computed, idade=10)
        interpretation = module.interpret(context, classified)

        self.assertEqual(classified["form_type"], "parent")
        self.assertTrue(all(item.get("nota_corte") is not None for item in classified["analise_geral"]))
        self.assertTrue(any(item.get("classificacao") == "Clínico" for item in classified["analise_geral"]))
        self.assertIn("SCARED - Pais/Cuidadores", interpretation)

    def test_validate_rejects_invalid_form(self):
        module = SCAREDModule()
        context = TestContext(
            patient_name="Paciente SCARED",
            evaluation_id=1,
            instrument_code="scared",
            patient_age=10,
            raw_scores={
                "form": "invalid",
                "responses": {str(i): 0 for i in range(1, 42)},
            },
        )

        errors = module.validate(context)
        self.assertIn("Formulário SCARED inválido.", errors)


class EPQJModuleTests(SimpleTestCase):
    def test_interpretation_mentions_desirability_when_sincerity_is_high(self):
        module = EPQJModule()
        context = TestContext(
            patient_name="Marina Costa",
            evaluation_id=1,
            instrument_code="epq_j",
        )

        interpretation = module.interpret(
            context,
            {
                "fatores": {
                    "P": {"escore": 2, "percentil": 40, "classificacao": "MEDIO"},
                    "E": {"escore": 10, "percentil": 50, "classificacao": "MEDIO"},
                    "N": {"escore": 8, "percentil": 50, "classificacao": "MEDIO"},
                    "S": {"escore": 16, "percentil": 99, "classificacao": "MUITO ALTO"},
                }
            },
        )

        self.assertIn("Sinceridade apresentou classificação muito alto (percentil 99)", interpretation)
        self.assertIn("desejabilidade social", interpretation)
        self.assertIn("não há elementos suficientes para sustentar hipótese diagnóstica específica", interpretation)

    def test_interpretation_builds_internalizing_profile(self):
        module = EPQJModule()
        context = TestContext(
            patient_name="Lucas Almeida",
            evaluation_id=1,
            instrument_code="epq_j",
        )

        interpretation = module.interpret(
            context,
            {
                "fatores": {
                    "P": {"escore": 1, "percentil": 20, "classificacao": "BAIXO"},
                    "E": {"escore": 6, "percentil": 10, "classificacao": "BAIXO"},
                    "N": {"escore": 16, "percentil": 90, "classificacao": "ALTO"},
                    "S": {"escore": 10, "percentil": 50, "classificacao": "MEDIO"},
                }
            },
        )

        self.assertIn("O escore alto em Neuroticismo (percentil 90)", interpretation)
        self.assertIn("funcionamento mais introspectivo", interpretation)
        self.assertIn("Em análise clínica, o perfil de Lucas no EPQ-J", interpretation)
        self.assertIn("há hipótese diagnóstica de vulnerabilidade emocional e sintomatologia ansiosa ou internalizante", interpretation)

    def test_interpretation_covers_all_required_sections(self):
        module = EPQJModule()
        context = TestContext(
            patient_name="Ana Silva",
            evaluation_id=1,
            instrument_code="epq_j",
        )

        interpretation = module.interpret(
            context,
            {
                "fatores": {
                    "P": {"escore": 0, "percentil": 5, "classificacao": "MUITO BAIXO"},
                    "E": {"escore": 12, "percentil": 90, "classificacao": "ALTO"},
                    "N": {"escore": 3, "percentil": 10, "classificacao": "BAIXO"},
                    "S": {"escore": 8, "percentil": 30, "classificacao": "MEDIO"},
                }
            },
        )

        self.assertIn("O resultado de Ana nesse fator", interpretation)
        self.assertIn("O fator Extroversão apresentou classificação alto (percentil 90)", interpretation)
        self.assertIn("O fator Sinceridade apresentou classificação médio (percentil 30)", interpretation)
        self.assertIn("Em análise clínica", interpretation)
        self.assertIn("Análise Clínica:", interpretation)
