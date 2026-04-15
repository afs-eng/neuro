from __future__ import annotations

from collections import Counter
from pathlib import Path
from dataclasses import asdict

from apps.tests.norms.bai import lookup_t_score, get_norms_metadata

from .charts import BAIChartBuilder
from .classifiers import BAIClassifier
from .constants import (
    ITEMS,
    RESPONSE_OPTIONS,
    RESPONSE_OPTIONS_SHORT,
    RESPONSE_OPTIONS_WITH_CODE,
)
from .interpreters import build_bai_interpretation
from .schemas import BAIComputedPayload, BAIItemResponse, BAIRawPayload
from .validators import BAIValidator


class BAICalculator:
    """
    Implementação do BAI para uso no sistema NeuroAvalia.

    Notas técnicas:
    - Escore bruto total: soma dos 21 itens (0 a 63)
    - Escore T: tabela normativa oficial (Amostra Geral, 18-90 anos)
    - Percentil: calculado a partir do escore T normativo
    """

    def __init__(self, chart_output_dir: str | Path | None = None):
        self.chart_output_dir = Path(chart_output_dir or "/tmp/bai_charts")

    def score(self, payload: BAIRawPayload) -> dict:
        """Calcula todos os escores do BAI a partir do raw payload."""
        BAIValidator.validate(payload)

        score_by_item = {item.item_number: item.score for item in payload.responses}
        ordered_scores = [score_by_item.get(i, 0) for i in range(1, len(ITEMS) + 1)]
        missing_count = sum(
            1 for i in range(1, len(ITEMS) + 1) if i not in score_by_item
        )
        total_raw_score = sum(ordered_scores)

        # Usa tabela normativa oficial
        t_score_int = lookup_t_score(total_raw_score)
        t_score = float(t_score_int) if t_score_int is not None else None
        percentile = (
            self.calculate_percentile_from_t(t_score) if t_score is not None else None
        )
        confidence_interval = (
            self.estimate_confidence_interval(t_score) if t_score is not None else None
        )
        faixa = BAIClassifier.classify_raw_score(total_raw_score)

        response_distribution = dict(Counter(ordered_scores))
        tables = self.build_tables(
            ordered_scores,
            total_raw_score,
            t_score,
            percentile,
            faixa,
            missing_count,
            confidence_interval,
        )

        computed_payload = BAIComputedPayload(
            total_raw_score=total_raw_score,
            t_score=t_score,
            percentile=percentile,
            confidence_interval=confidence_interval,
            missing_count=missing_count,
            faixa_normativa=faixa["label"],
            interpretacao_faixa=faixa["interpretation"],
            response_distribution=response_distribution,
            tables=tables,
            chart_payload={
                "raw_score": total_raw_score,
                "t_score": t_score,
                "percentile": percentile,
                "confidence_interval": confidence_interval,
                "missing_count": missing_count,
                "faixa_normativa": faixa["label"],
                "interpretacao_faixa": faixa["interpretation"],
            },
        )

        result = asdict(computed_payload)
        chart_builder = BAIChartBuilder(self.chart_output_dir)
        charts = chart_builder.build_all(result)

        result["charts"] = charts
        result["interpretation_text"] = build_bai_interpretation(
            result, payload.respondent_name
        )
        return result

    def compute_from_dict(self, raw_scores: dict, patient_name: str = "") -> dict:
        """Calcula a partir de um dicionário simples (uso via TestContext)."""
        responses = []
        for i in range(1, 22):
            key = f"item_{i:02d}"
            score = raw_scores.get(key, 0)
            responses.append(BAIItemResponse(item_number=i, score=score))

        payload = BAIRawPayload(
            respondent_name=patient_name,
            application_mode="system",
            responses=responses,
        )
        return self.score(payload)

    @staticmethod
    def calculate_percentile_from_t(t_score: float) -> float:
        """
        Calcula percentil a partir do escore T usando distribuição normal padrão.
        T-score: média=50, DP=10
        """
        import math

        z = (t_score - 50) / 10
        percentile = 100 / (1 + math.exp(-1.7 * z))
        return round(percentile, 1)

    @staticmethod
    def estimate_confidence_interval(t_score: float) -> list[float]:
        """Intervalo de confiança estimado (±5 pontos T)."""
        return [round(max(20, t_score - 5), 1), round(min(80, t_score + 5), 1)]

    def build_tables(
        self,
        ordered_scores: list[int],
        total_raw_score: int,
        t_score: float,
        percentile: float,
        faixa: dict,
        missing_count: int,
        confidence_interval: list[float],
    ) -> dict:
        """Constrói todas as tabelas de saída do BAI."""
        # Tabela de itens
        items_table = []
        for idx, score in enumerate(ordered_scores, start=1):
            items_table.append(
                {
                    "item": idx,
                    "item_short": ITEMS[idx - 1],
                    "label": ITEMS[idx - 1],
                    "response_code": score,
                    "response_display_code": score + 1,
                    "response_value": score,
                    "response_label": RESPONSE_OPTIONS[score],
                    "response_label_short": RESPONSE_OPTIONS_SHORT[score],
                    "response_label_with_code": RESPONSE_OPTIONS_WITH_CODE[score],
                    "points": score,
                }
            )

        # Tabela resumo
        summary_table = [
            {
                "scale": "Escore Total",
                "raw_score": total_raw_score,
                "norm_value": int(t_score) if t_score else None,
                "classification": faixa["label"],
                "description": faixa["interpretation"],
                "percentile": percentile,
                "missing": missing_count,
                "confidence_interval": f"[{int(confidence_interval[0])} - {int(confidence_interval[1])}]",
            }
        ]

        detail_table = [
            {"label": "Pontuação bruta", "value": total_raw_score},
            {
                "label": "Valor da norma",
                "value": int(t_score) if t_score is not None else "-",
            },
            {"label": "Respostas faltantes (missing)", "value": missing_count},
            {
                "label": "Intervalo de confiança",
                "value": f"[{int(confidence_interval[0])} - {int(confidence_interval[1])}]"
                if confidence_interval
                else "-",
            },
        ]

        # Tabela de classificação
        classification_table = [
            {
                "classification": "Mínimo",
                "description": "Nível mínimo de ansiedade",
                "range": "0-10",
            },
            {
                "classification": "Leve",
                "description": "Nível brando de ansiedade",
                "range": "11-19",
            },
            {
                "classification": "Moderado",
                "description": "Nível moderado de ansiedade",
                "range": "20-30",
            },
            {
                "classification": "Grave",
                "description": "Nível severo de ansiedade",
                "range": "31-63",
            },
        ]

        # Tabela de distribuição
        distribution_table = []
        counter = Counter(ordered_scores)
        total = len(ordered_scores) or 1
        for response_code in range(4):
            count = counter.get(response_code, 0)
            distribution_table.append(
                {
                    "response": response_code,
                    "response_display_code": response_code + 1,
                    "label": RESPONSE_OPTIONS[response_code],
                    "label_short": RESPONSE_OPTIONS_SHORT[response_code],
                    "count": count,
                    "percent": round((count / total) * 100, 1),
                }
            )

        return {
            "summary_table": summary_table,
            "detail_table": detail_table,
            "classification_table": classification_table,
            "items_table": items_table,
            "distribution_table": distribution_table,
        }
