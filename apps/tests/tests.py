from django.test import SimpleTestCase

from apps.tests.bai import BAIModule
from apps.tests.base.types import TestContext
from apps.tests.cars2_hf import CARS2HFModule
from apps.tests.cars2_hf.classifiers import classify_cars2_hf
from apps.tests.cars2_hf.loaders import load_cars2_hf_norms
from apps.tests.mchat import MCHATModule
from apps.tests.mchat.constants import FAILURE_RULES, ITEMS
from apps.tests.norms.bai import get_norms_metadata, lookup_t_score


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
