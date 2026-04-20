from django.test import SimpleTestCase

from apps.reports.builders.references_builder import build_references
from apps.reports.services.report_export_service import ReportExportService
from apps.reports.services.wisc4_standardization import WISC4StandardizationService


class ReferencesBuilderTests(SimpleTestCase):
    def test_build_references_includes_only_validated_tests(self):
        references = build_references(
            [
                {"instrument_code": "wisc4"},
                {"instrument_code": "fdt"},
            ]
        )

        self.assertEqual(len(references), 3)
        self.assertIn("WISC-IV", references[1])
        self.assertIn("Teste dos Cinco Dígitos", references[2])

    def test_build_references_deduplicates_equivalent_entries(self):
        references = build_references(
            [
                {"instrument_code": "ebadep_ij"},
                {"instrument_code": "ebaped_ij"},
            ]
        )

        self.assertEqual(len(references), 2)
        self.assertIn("EBADEP-IJ", references[1])


class WISC4StandardizationTests(SimpleTestCase):
    def setUp(self):
        self.context = {
            "patient": {"full_name": "Maria Clara", "sex": "F"},
            "validated_tests": [
                {
                    "instrument_code": "wisc4",
                    "structured_results": {
                        "qit_data": {
                            "escore_composto": 61,
                            "classificacao": "Extremamente Baixo",
                        },
                        "gai_data": {
                            "escore_composto": 70,
                            "classificacao": "Limítrofe",
                        },
                        "cpi_data": {
                            "escore_composto": 58,
                            "classificacao": "Extremamente Baixo",
                        },
                        "indices": [
                            {
                                "indice": "icv",
                                "escore_composto": 84,
                                "classificacao": "Média Inferior",
                            },
                            {
                                "indice": "iop",
                                "escore_composto": 61,
                                "classificacao": "Extremamente Baixo",
                            },
                            {
                                "indice": "imt",
                                "escore_composto": 52,
                                "classificacao": "Extremamente Baixo",
                            },
                            {
                                "indice": "ivp",
                                "escore_composto": 68,
                                "classificacao": "Extremamente Baixo",
                            },
                        ],
                        "subtestes": [
                            {"codigo": "SM", "classificacao": "Média"},
                            {"codigo": "CN", "classificacao": "Média Inferior"},
                            {"codigo": "CO", "classificacao": "Média"},
                            {"codigo": "RM", "classificacao": "Limítrofe"},
                            {"codigo": "VC", "classificacao": "Limítrofe"},
                            {"codigo": "CB", "classificacao": "Extremamente Baixo"},
                            {"codigo": "SNL", "classificacao": "Extremamente Baixo"},
                            {"codigo": "DG", "classificacao": "Limítrofe"},
                        ],
                    },
                }
            ],
        }

    def test_build_global_section_uses_standardized_wisc_template(self):
        text = WISC4StandardizationService.build(
            "capacidade_cognitiva_global", self.context
        )

        self.assertIn("Capacidade Cognitiva Global: A paciente obteve", text)
        self.assertIn("QI Total (QIT 61)", text)
        self.assertIn("Compreensão Verbal (ICV) — 84 — Média Inferior", text)
        self.assertNotIn("Índice de Habilidade Geral (GAI = 70)", text)
        self.assertNotIn("O Índice de Compreensão Verbal", text)

    def test_build_global_section_includes_fixed_cognitive_age_phrase_when_available(self):
        self.context["validated_tests"][0]["structured_results"]["idade_cognitiva"] = "12 anos e 6 meses"

        text = WISC4StandardizationService.build(
            "capacidade_cognitiva_global", self.context
        )

        self.assertIn(
            "quando comparado à média geral e com idade cognitiva estimada de 12 anos e 6 meses",
            text,
        )

    def test_build_domain_section_uses_standardized_wisc_subscale_template(self):
        text = WISC4StandardizationService.build("funcoes_executivas", self.context)

        self.assertIn("A avaliação das funções executivas de Maria", text)
        self.assertIn("No subteste Semelhanças", text)
        self.assertIn("No subteste Raciocínio Matricial", text)
        self.assertIn("perfil executivo heterogêneo", text)


class WISC4ExportTableTests(SimpleTestCase):
    def setUp(self):
        self.context = {
            "patient": {"birth_date": "2016-01-10"},
            "evaluation": {"start_date": "2024-04-20"},
            "validated_tests": [
                {
                    "instrument_code": "wisc4",
                    "applied_on": "2024-04-20",
                }
            ],
        }
        self.test = {
            "classified_payload": {
                "subtestes": [
                    {
                        "codigo": "SM",
                        "subteste": "Semelhanças",
                        "escore_bruto": 23,
                        "classificacao": "Média",
                    },
                    {
                        "codigo": "CN",
                        "subteste": "Conceitos Figurativos",
                        "escore_bruto": 11,
                        "classificacao": "Média Inferior",
                    },
                    {
                        "codigo": "CO",
                        "subteste": "Compreensão",
                        "escore_bruto": 24,
                        "classificacao": "Média",
                    },
                    {
                        "codigo": "RM",
                        "subteste": "Raciocínio Matricial",
                        "escore_bruto": 12,
                        "classificacao": "Limítrofe",
                    },
                ]
            }
        }

    def test_wisc_reference_scores_use_age_norm_table_ranges(self):
        table = ReportExportService._wisc_ncp_table(self.context)

        self.assertEqual(
            ReportExportService._wisc_reference_scores(table, "SM"),
            ("32-44", "6-16", "1"),
        )

    def test_wisc_rows_build_expected_columns_for_executive_domain(self):
        rows = ReportExportService._wisc_rows(
            self.test, self.context, "funcoes_executivas"
        )

        self.assertEqual(
            rows[0],
            [
                "Testes Utilizados",
                "Escore Máximo",
                "Escore Médio",
                "Escore Mínimo",
                "Escore Bruto",
                "Classificação",
            ],
        )
        self.assertEqual(rows[1], ["Semelhanças", "32-44", "6-16", "1", "23", "Média"])
