from __future__ import annotations

from io import BytesIO
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


def _render_bpa_chart(
    atencao_concentrada: dict,
    atencao_dividida: dict,
    atencao_alternada: dict,
    atencao_geral: dict,
    titulo: str,
    dpi: int,
) -> bytes:
    categorias = [
        "Escore Máximo",
        "Escore Médio",
        "Escore Mínimo",
        "Escore Bruto",
        "Percentil Obtido",
    ]
    ordem = ["maximo", "medio", "minimo", "bruto", "percentil"]

    concentrada = [float(atencao_concentrada.get(chave, 0) or 0) for chave in ordem]
    dividida = [float(atencao_dividida.get(chave, 0) or 0) for chave in ordem]
    alternada = [float(atencao_alternada.get(chave, 0) or 0) for chave in ordem]
    geral = [float(atencao_geral.get(chave, 0) or 0) for chave in ordem]

    x = np.arange(len(categorias))
    largura = 0.17

    fig, ax = plt.subplots(figsize=(14, 6), dpi=dpi)
    fig.patch.set_facecolor("white")
    fig.patch.set_edgecolor("#BFBFBF")
    fig.patch.set_linewidth(1.2)
    ax.set_facecolor("white")

    b1 = ax.bar(
        x - 1.5 * largura,
        concentrada,
        largura,
        color="#E67E22",
        label="ATENÇÃO CONCENTRADA",
        linewidth=0,
    )
    b2 = ax.bar(
        x - 0.5 * largura,
        dividida,
        largura,
        color="#F1B500",
        label="ATENÇÃO DIVIDIDA",
        linewidth=0,
    )
    b3 = ax.bar(
        x + 0.5 * largura,
        alternada,
        largura,
        color="#7BAE45",
        label="ATENÇÃO ALTERNADA",
        linewidth=0,
    )
    b4 = ax.bar(
        x + 1.5 * largura,
        geral,
        largura,
        color="#A94F0B",
        label="ATENÇÃO GERAL",
        linewidth=0,
    )

    ax.set_title(
        titulo,
        fontsize=22,
        color="#5D7F3A",
        pad=20,
        fontname="DejaVu Serif",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(categorias, fontsize=12, fontname="DejaVu Serif")

    ymax = max(
        max(concentrada or [0]),
        max(dividida or [0]),
        max(alternada or [0]),
        max(geral or [0]),
    )
    ax.set_ylim(0, ymax + 70)
    ax.tick_params(axis="y", labelsize=11, colors="#555555")
    ax.tick_params(axis="x", colors="#555555")

    ax.grid(axis="y", linestyle="-", alpha=0.35, color="gray")
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    def adicionar_rotulos(barras):
        for barra in barras:
            altura = float(barra.get_height())
            rotulo = (
                str(int(altura))
                if altura.is_integer()
                else f"{altura:.2f}".rstrip("0").rstrip(".")
            )
            ax.text(
                barra.get_x() + barra.get_width() / 2,
                altura + 3,
                rotulo,
                ha="center",
                va="bottom",
                fontsize=12,
                fontname="DejaVu Serif",
                color="#444444",
            )

    adicionar_rotulos(b1)
    adicionar_rotulos(b2)
    adicionar_rotulos(b3)
    adicionar_rotulos(b4)

    ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, -0.28),
        ncol=4,
        frameon=False,
        fontsize=12,
        handlelength=0.6,
        handletextpad=0.3,
    )

    output = BytesIO()
    plt.tight_layout()
    fig.savefig(output, format="png", dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return output.getvalue()


def gerar_grafico_bpa(
    output_path,
    atencao_concentrada,
    atencao_dividida,
    atencao_alternada,
    atencao_geral,
    titulo="BPA - BATERIA PSICOLÓGICA PARA AVALIAÇÃO DA ATENÇÃO",
    dpi=300,
) -> str:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(
        _render_bpa_chart(
            atencao_concentrada=atencao_concentrada,
            atencao_dividida=atencao_dividida,
            atencao_alternada=atencao_alternada,
            atencao_geral=atencao_geral,
            titulo=titulo,
            dpi=dpi,
        )
    )
    return str(output)


def gerar_grafico_bpa_bytes(chart_data: dict, dpi: int = 300) -> bytes | None:
    domains = chart_data.get("domains") or []
    by_label = {item.get("label"): item.get("values") or {} for item in domains}
    required = [
        "ATENÇÃO CONCENTRADA",
        "ATENÇÃO DIVIDIDA",
        "ATENÇÃO ALTERNADA",
        "ATENÇÃO GERAL",
    ]
    if not all(label in by_label for label in required):
        return None

    return _render_bpa_chart(
        atencao_concentrada=by_label["ATENÇÃO CONCENTRADA"],
        atencao_dividida=by_label["ATENÇÃO DIVIDIDA"],
        atencao_alternada=by_label["ATENÇÃO ALTERNADA"],
        atencao_geral=by_label["ATENÇÃO GERAL"],
        titulo=chart_data.get("title") or "BPA - BATERIA PSICOLÓGICA PARA AVALIAÇÃO DA ATENÇÃO",
        dpi=dpi,
    )
