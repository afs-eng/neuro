from __future__ import annotations

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")


def gerar_grafico_wasi_bytes(
    qi_verbal: int,
    qi_execucao: int,
    qi_total: int,
    dpi: int = 300,
) -> bytes | None:
    labels = ["QI verbal", "QI Execução", "QI Total"]
    valores = [qi_verbal, qi_execucao, qi_total]
    cores = ["#4472C4", "#ED7D31", "#70AD47"]

    plt.rcParams["font.family"] = "Times New Roman"

    fig, ax = plt.subplots(figsize=(9.8, 4.0), dpi=dpi)

    ax.axhspan(90, 110, color="#F4C2F4", alpha=0.35, zorder=0)

    barras = ax.bar(labels, valores, color=cores, width=0.32, zorder=2)

    for barra, valor in zip(barras, valores):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            valor + 3,
            str(valor),
            ha="center",
            va="bottom",
            fontsize=10,
            color="#333333",
        )

    ax.set_title("WASI QIs", fontsize=18, color="#2F4F1F", pad=10)
    ax.set_ylim(10, 130)
    ax.set_yticks([10, 30, 50, 70, 90, 110, 130])

    ax.tick_params(axis="x", labelsize=10, colors="#4D4D4D")
    ax.tick_params(axis="y", labelsize=9, colors="#4D4D4D", length=0)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#CFCFCF")
    ax.spines["bottom"].set_linewidth(0.8)

    ax.grid(False)

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

    labels = ["QI verbal", "QI Execução", "QI Total"]
    valores = [qi_verbal, qi_execucao, qi_total]
    cores = ["#4472C4", "#ED7D31", "#70AD47"]

    plt.rcParams["font.family"] = "Times New Roman"

    fig, ax = plt.subplots(figsize=(9.8, 4.0), dpi=300)

    ax.axhspan(90, 110, color="#F4C2F4", alpha=0.35, zorder=0)

    barras = ax.bar(labels, valores, color=cores, width=0.32, zorder=2)

    for barra, valor in zip(barras, valores):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            valor + 3,
            str(valor),
            ha="center",
            va="bottom",
            fontsize=10,
            color="#333333",
        )

    ax.set_title("WASI QIs", fontsize=18, color="#2F4F1F", pad=10)
    ax.set_ylim(10, 130)
    ax.set_yticks([10, 30, 50, 70, 90, 110, 130])

    ax.tick_params(axis="x", labelsize=10, colors="#4D4D4D")
    ax.tick_params(axis="y", labelsize=9, colors="#4D4D4D", length=0)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#CFCFCF")
    ax.spines["bottom"].set_linewidth(0.8)

    ax.grid(False)

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
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    return output_path