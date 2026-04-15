from __future__ import annotations

from collections import Counter
from pathlib import Path
from dataclasses import asdict

from .classifiers import BAIClassifier
from .constants import ITEMS, RESPONSE_LABELS_WITH_CODE, RESPONSE_OPTIONS
from .charts import BAIChartBuilder
from .interpreters import build_bai_interpretation
from .schemas import BAIComputedPayload, BAIRawPayload
from .validators import BAIValidator


class BAICalculator:
    """
    Implementação pragmática do BAI para uso no sistema.

    Observação técnica:
    - escore bruto total: soma dos 21 itens (0 a 63)
    - escore T e percentil: por padrão, são estimados a partir de parâmetros
      configuráveis do sistema (média=50, DP=10) e de uma curva logística suave.
    - quando houver tabela normativa oficial estruturada no projeto, substitua
      os métodos estimate_t_score e estimate_percentile por lookup exato.
    """

    def __init__(self, chart_output_dir: str | Path | None = None):
        self.chart_output_dir = Path(chart_output_dir or "/tmp/bai_charts")

    def score(self, payload: BAIRawPayload) -> dict:
        BAIValidator.validate(payload)

        score_by_item = {item.item_number: item.score for item in payload.responses}
        ordered_scores = [score_by_item.get(i, 0) for i in range(1, len(ITEMS) + 1)]
        missing_count = sum(1 for i in range(1, len(ITEMS) + 1) if i not in score_by_item)
        total_raw_score = sum(ordered_scores)

        t_score = self.estimate_t_score(total_raw_score)
        percentile = self.estimate_percentile(t_score) if t_score is not None else None
        confidence_interval = self.estimate_confidence_interval(t_score) if t_score is not None else None
        faixa = BAIClassifier.classify_raw_score(total_raw_score)

        response_distribution = dict(Counter(ordered_scores))
        tables = self.build_tables(ordered_scores, total_raw_score, t_score, percentile, faixa, missing_count, confidence_interval)

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
                "faixa_normativa": faixa["label"],
            },
        )

        result = asdict(computed_payload)
        chart_builder = BAIChartBuilder(self.chart_output_dir)
        charts = chart_builder.build_all(result)

        result["charts"] = charts
        result["interpretation_text"] = build_bai_interpretation(result, payload.respondent_name)
        return result

    @staticmethod
    def estimate_t_score(raw_score: int) -> float:
        # Heurística inicial: mapeia 0..63 aproximadamente para T=35..80.
        return round(35 + (raw_score / 63) * 45, 0)

    @staticmethod
    def estimate_percentile(t_score: float) -> float:
        # Aproximação logística para interface e relatórios. Substituir por lookup oficial quando disponível.
        import math
        z = (t_score - 50) / 10
        percentile = 100 / (1 + math.exp(-1.7 * z))
        return round(percentile, 1)

    @staticmethod
    def estimate_confidence_interval(t_score: float) -> list[float]:
        return [round(max(20, t_score - 5), 0), round(min(80, t_score + 5), 0)]

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
        items_table = []
        for idx, score in enumerate(ordered_scores, start=1):
            items_table.append(
                {
                    "nr": idx,
                    "item_abreviado": ITEMS[idx - 1],
                    "resposta": RESPONSE_LABELS_WITH_CODE[score],
                    "pontos": score,
                }
            )

        summary_table = [
            {
                "escala": "Escore Total",
                "pontuacao_bruta": total_raw_score,
                "valor_da_norma": int(t_score),
                "faixa_normativa": faixa["label"],
                "interpretacao": faixa["interpretation"],
                "percentil": percentile,
                "missing": missing_count,
                "intervalo_confianca": f"[{int(confidence_interval[0])} - {int(confidence_interval[1])}]",
            }
        ]

        classification_table = [
            {"faixa_normativa": "Mínimo", "interpretacao": "Nível mínimo de ansiedade"},
            {"faixa_normativa": "Leve", "interpretacao": "Nível brando de ansiedade"},
            {"faixa_normativa": "Moderado", "interpretacao": "Nível moderado de ansiedade"},
            {"faixa_normativa": "Grave", "interpretacao": "Nível severo de ansiedade"},
        ]

        distribution_table = []
        counter = Counter(ordered_scores)
        total = len(ordered_scores) or 1
        for response_code in range(4):
            count = counter.get(response_code, 0)
            distribution_table.append(
                {
                    "resposta": response_code,
                    "descricao": RESPONSE_OPTIONS[response_code],
                    "quantidade": count,
                    "percentual": round((count / total) * 100, 1),
                }
            )

        return {
            "summary_table": summary_table,
            "classification_table": classification_table,
            "items_table": items_table,
            "distribution_table": distribution_table,
        }
