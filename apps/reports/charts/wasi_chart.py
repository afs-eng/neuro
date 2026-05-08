from __future__ import annotations

import matplotlib
import matplotlib.pyplot as plt

from apps.reports.specs import WASI_CHART_SPEC, WASI_LAYOUT_SPEC

matplotlib.use("Agg")


def gerar_grafico_wasi_bytes(
    qi_verbal: int,
    qi_execucao: int,
    qi_total: int,
    dpi: int = 300,
) -> bytes | None:
    labels = WASI_CHART_SPEC["labels"]
    valores = [qi_verbal, qi_execucao, qi_total]
    cores = ["#4472C4", "#ED7D31", "#70AD47"]

    plt.rcParams["font.family"] = WASI_LAYOUT_SPEC["font_family"]

    fig, ax = plt.subplots(figsize=(9.8, 4.0), dpi=dpi)
    fig.patch.set_facecolor(WASI_CHART_SPEC["background_color"])

    ax.axhspan(
        *WASI_CHART_SPEC["average_band"],
        color=WASI_CHART_SPEC["average_band_color"],
        alpha=0.35,
        zorder=0,
    )

    barras = ax.bar(labels, valores, color=cores, width=0.32, zorder=2)

    for barra, valor in zip(barras, valores):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            valor + 3,
            str(valor),
            ha="center",
            va="bottom",
            fontsize=WASI_CHART_SPEC["data_label_size_pt"],
            color="#333333",
        )

    ax.set_title(
        WASI_CHART_SPEC["title"],
        fontsize=WASI_CHART_SPEC["title_size_pt"],
        color="#2F4F1F",
        pad=10,
    )
    ax.set_ylabel(
        WASI_CHART_SPEC["y_label"],
        fontsize=WASI_CHART_SPEC["axis_label_size_pt"],
    )
    ax.set_ylim(10, 130)
    ax.set_yticks([10, 30, 50, 70, 90, 110, 130])

    ax.tick_params(
        axis="x",
        labelsize=WASI_CHART_SPEC["axis_label_size_pt"],
        colors="#4D4D4D",
    )
    ax.tick_params(
        axis="y",
        labelsize=WASI_CHART_SPEC["axis_label_size_pt"],
        colors="#4D4D4D",
        length=0,
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#CFCFCF")
    ax.spines["bottom"].set_linewidth(0.8)

    ax.grid(axis="y", color="#D9D9D9", linewidth=0.8)

    ax.plot([2.18, 2.48], [74, 74], color="#F4A3F4", linewidth=5, solid_capstyle="butt")
    ax.text(
        2.33,
        61,
        "Média",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        bbox=dict(facecolor="white", edgecolor="#CFCFCF", boxstyle="square,pad=0.45"),
    )

    plt.tight_layout()

    from io import BytesIO

    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return buffer.getvalue()


def gerar_grafico_wasi(
    qi_verbal: int,
    qi_execucao: int,
    qi_total: int,
    output_path: str = "wasi_qis.png",
) -> str:
    """Gera o gráfico WASI e salva em arquivo."""
    import matplotlib
    import matplotlib.pyplot as plt

    matplotlib.use("Agg")

    labels = WASI_CHART_SPEC["labels"]
    valores = [qi_verbal, qi_execucao, qi_total]
    cores = ["#4472C4", "#ED7D31", "#70AD47"]

    plt.rcParams["font.family"] = WASI_LAYOUT_SPEC["font_family"]

    fig, ax = plt.subplots(figsize=(9.8, 4.0), dpi=300)
    fig.patch.set_facecolor(WASI_CHART_SPEC["background_color"])

    ax.axhspan(
        *WASI_CHART_SPEC["average_band"],
        color=WASI_CHART_SPEC["average_band_color"],
        alpha=0.35,
        zorder=0,
    )

    barras = ax.bar(labels, valores, color=cores, width=0.32, zorder=2)

    for barra, valor in zip(barras, valores):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            valor + 3,
            str(valor),
            ha="center",
            va="bottom",
            fontsize=WASI_CHART_SPEC["data_label_size_pt"],
            color="#333333",
        )

    ax.set_title(
        WASI_CHART_SPEC["title"],
        fontsize=WASI_CHART_SPEC["title_size_pt"],
        color="#2F4F1F",
        pad=10,
    )
    ax.set_ylabel(
        WASI_CHART_SPEC["y_label"],
        fontsize=WASI_CHART_SPEC["axis_label_size_pt"],
    )
    ax.set_ylim(10, 130)
    ax.set_yticks([10, 30, 50, 70, 90, 110, 130])

    ax.tick_params(
        axis="x",
        labelsize=WASI_CHART_SPEC["axis_label_size_pt"],
        colors="#4D4D4D",
    )
    ax.tick_params(
        axis="y",
        labelsize=WASI_CHART_SPEC["axis_label_size_pt"],
        colors="#4D4D4D",
        length=0,
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#CFCFCF")
    ax.spines["bottom"].set_linewidth(0.8)

    ax.grid(axis="y", color="#D9D9D9", linewidth=0.8)

    ax.plot([2.18, 2.48], [74, 74], color="#F4A3F4", linewidth=5, solid_capstyle="butt")
    ax.text(
        2.33,
        61,
        "Média",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        bbox=dict(facecolor="white", edgecolor="#CFCFCF", boxstyle="square,pad=0.45"),
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    return output_path
