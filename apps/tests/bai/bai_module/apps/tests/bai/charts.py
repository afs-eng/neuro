from __future__ import annotations

from math import exp, pi, sqrt
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt


class BAIChartBuilder:
    def __init__(self, output_dir: str | Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build_all(self, computed_payload: dict) -> dict:
        return {
            "profile_chart": str(self.profile_chart(computed_payload)),
            "detail_chart": str(self.detail_chart(computed_payload)),
            "distribution_chart": str(self.distribution_chart(computed_payload)),
        }

    def profile_chart(self, computed_payload: dict) -> Path:
        t_score = computed_payload.get("t_score") or 50
        raw_score = computed_payload["total_raw_score"]
        x_ticks = list(range(20, 85, 5))

        fig, ax = plt.subplots(figsize=(10, 2.8))
        ax.set_xlim(20, 80)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_xticks(x_ticks)
        ax.set_title("Perfil - Escore T do BAI", loc="left", fontsize=16, fontweight="bold")

        for x in range(20, 80, 5):
            ax.axvline(x, ymin=0.1, ymax=0.7, linewidth=0.8)

        ax.scatter([t_score], [0.35], s=36, zorder=3)
        ax.text(20.5, 0.12, f"EB {raw_score}", fontsize=10)
        ax.text(min(max(t_score + 0.8, 20.5), 76), 0.12, f"T {t_score:.0f}", fontsize=10)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.set_xlabel("Escore T")

        path = self.output_dir / "bai_profile_chart.png"
        fig.tight_layout()
        fig.savefig(path, dpi=200, bbox_inches="tight")
        plt.close(fig)
        return path

    def detail_chart(self, computed_payload: dict) -> Path:
        t_score = computed_payload.get("t_score") or 50
        xs = [x / 10 for x in range(200, 801)]
        ys = [self._normal_pdf(x, 50, 10) for x in xs]

        fig, ax = plt.subplots(figsize=(8.5, 4))
        ax.plot(xs, ys)
        ax.fill_between(xs, ys, alpha=0.15)
        y_mark = self._normal_pdf(t_score, 50, 10)
        ax.scatter([t_score], [y_mark], s=36, zorder=3)
        ax.set_title("Detalhes da escala - Curva normativa", loc="left", fontsize=16, fontweight="bold")
        ax.set_xlabel("Escore T")
        ax.set_ylabel("Densidade")
        ax.spines[["top", "right"]].set_visible(False)

        path = self.output_dir / "bai_detail_chart.png"
        fig.tight_layout()
        fig.savefig(path, dpi=200, bbox_inches="tight")
        plt.close(fig)
        return path

    def distribution_chart(self, computed_payload: dict) -> Path:
        distribution = computed_payload["response_distribution"]
        labels = ["0", "1", "2", "3"]
        counts = [distribution.get(i, 0) for i in range(4)]
        total = sum(counts) or 1
        percentages = [(count / total) * 100 for count in counts]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(labels, percentages)
        ax.set_ylim(0, 100)
        ax.set_title("Estatísticas das respostas", loc="left", fontsize=16, fontweight="bold")
        ax.set_xlabel("Resposta")
        ax.set_ylabel("Percentual")
        ax.spines[["top", "right"]].set_visible(False)

        for idx, value in enumerate(percentages):
            ax.text(idx, value + 1.5, f"{value:.0f}%", ha="center", va="bottom", fontsize=9)

        path = self.output_dir / "bai_distribution_chart.png"
        fig.tight_layout()
        fig.savefig(path, dpi=200, bbox_inches="tight")
        plt.close(fig)
        return path

    @staticmethod
    def _normal_pdf(x: float, mean: float, std_dev: float) -> float:
        coefficient = 1 / (std_dev * sqrt(2 * pi))
        exponent = exp(-0.5 * ((x - mean) / std_dev) ** 2)
        return coefficient * exponent
