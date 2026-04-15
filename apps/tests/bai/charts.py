from __future__ import annotations

from math import exp, pi, sqrt
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


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
        """Gráfico de perfil do escore T do BAI no estilo do relatório modelo."""
        t_score = computed_payload.get("t_score") or 50
        raw_score = computed_payload["total_raw_score"]
        fig, ax = plt.subplots(figsize=(11.5, 3.2))
        ax.set_xlim(16, 108)
        ax.set_ylim(0, 1)
        ax.axis("off")

        start_x = 20
        end_x = 80
        cell_height = 0.28
        cell_y = 0.34
        tick_values = list(range(20, 81, 5))

        ax.text(
            16, 0.92, "Inventário de Ansiedade · Padrão", fontsize=10, fontweight="bold"
        )
        ax.text(
            16,
            0.82,
            "Amostra Geral · Escore T (50+10z)",
            fontsize=10,
            fontweight="bold",
        )

        ax.add_patch(
            Rectangle(
                (16, cell_y), 6, cell_height, facecolor="#dff5f7", edgecolor="#ffffff"
            )
        )
        ax.add_patch(
            Rectangle(
                (22, cell_y), 6, cell_height, facecolor="#dff5f7", edgecolor="#ffffff"
            )
        )
        ax.text(
            19,
            cell_y + cell_height / 2,
            f"{raw_score}",
            ha="center",
            va="center",
            fontsize=10,
        )
        ax.text(
            25,
            cell_y + cell_height / 2,
            f"{t_score:.0f}",
            ha="center",
            va="center",
            fontsize=10,
        )

        segment_width = (end_x - start_x) / 12
        for idx in range(12):
            x0 = 28 + idx * segment_width
            ax.add_patch(
                Rectangle(
                    (x0, cell_y),
                    segment_width,
                    cell_height,
                    facecolor="#b8b8b8" if idx % 2 == 0 else "#a7a7a7",
                    edgecolor="#ffffff",
                    linewidth=0.8,
                )
            )

        ax.add_patch(
            Rectangle(
                (88, cell_y), 18, cell_height, facecolor="#dff5f7", edgecolor="#ffffff"
            )
        )
        ax.text(
            89,
            cell_y + cell_height / 2,
            "Escore Total",
            va="center",
            fontsize=10,
            fontweight="bold",
        )

        for value in tick_values:
            x = 28 + ((value - start_x) / (end_x - start_x)) * 60
            ax.plot([x, x], [0.64, 0.69], color="#555555", linewidth=0.8)
            ax.text(x, 0.73, f"{value}", ha="center", va="bottom", fontsize=8)

        for label, value in [
            ("min", 20),
            ("-s", 40),
            ("m", 50),
            ("+s", 60),
            ("max", 80),
        ]:
            x = 28 + ((value - start_x) / (end_x - start_x)) * 60
            ax.text(x, 0.78, label, ha="center", va="bottom", fontsize=10)

        point_x = 28 + ((t_score - start_x) / (end_x - start_x)) * 60
        ax.scatter(
            [point_x], [cell_y + cell_height / 2], s=48, color="#e11d48", zorder=3
        )
        ax.text(17.2, 0.59, "Dados brutos", rotation=90, fontsize=8, va="center")

        path = self.output_dir / "bai_profile_chart.png"
        fig.tight_layout()
        fig.savefig(path, dpi=200, bbox_inches="tight")
        plt.close(fig)
        return path

    def detail_chart(self, computed_payload: dict) -> Path:
        """Curva normativa do escore T do BAI no estilo do relatório modelo."""
        t_score = computed_payload.get("t_score") or 50
        confidence_interval = computed_payload.get("confidence_interval") or [
            max(20, t_score - 5),
            min(80, t_score + 5),
        ]
        xs = [x / 10 for x in range(200, 801)]
        ys = [self._normal_pdf(x, 50, 10) for x in xs]

        fig, ax = plt.subplots(figsize=(8.5, 4.2))
        ax.plot(xs, ys, color="#8aa6ac", linewidth=1.4)
        ax.fill_between(xs, ys, alpha=0.18, color="#c8eef2")
        y_mark = self._normal_pdf(t_score, 50, 10)
        ax.vlines(t_score, 0, y_mark, color="#e11d48", linewidth=2)
        ax.scatter([t_score], [y_mark], s=36, color="#e11d48", zorder=3)
        ax.hlines(0, 20, 80, color="#111827", linewidth=1)
        ax.plot(
            [confidence_interval[0], confidence_interval[1]],
            [0.0009, 0.0009],
            color="#b6e7eb",
            linewidth=5,
            solid_capstyle="round",
        )
        ax.set_xlim(18, 82)
        ax.set_ylim(0, max(ys) * 1.15)
        ax.set_xticks(list(range(20, 81, 10)))
        ax.set_yticks([])
        ax.set_title(
            "Detalhes da escala - Curva normativa",
            loc="left",
            fontsize=16,
            fontweight="bold",
        )
        ax.spines[["top", "right", "left"]].set_visible(False)

        path = self.output_dir / "bai_detail_chart.png"
        fig.tight_layout()
        fig.savefig(path, dpi=200, bbox_inches="tight")
        plt.close(fig)
        return path

    def distribution_chart(self, computed_payload: dict) -> Path:
        """Gráfico de distribuição das respostas do BAI."""
        distribution = computed_payload["response_distribution"]
        labels = ["1", "2", "3", "4"]
        counts = [distribution.get(i, 0) for i in range(4)]
        total = sum(counts) or 1
        percentages = [(count / total) * 100 for count in counts]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(labels, percentages, color="#c8eef2", edgecolor="#94a3b8")
        ax.set_ylim(0, 100)
        ax.set_title(
            "Estatísticas das respostas", loc="left", fontsize=16, fontweight="bold"
        )
        ax.set_xlabel("Resposta")
        ax.set_ylabel("Percentual")
        ax.spines[["top", "right"]].set_visible(False)

        for idx, value in enumerate(percentages):
            ax.text(
                idx, value + 1.5, f"{value:.0f}%", ha="center", va="bottom", fontsize=9
            )

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
