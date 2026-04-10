
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.path import Path
from matplotlib.patches import PathPatch

try:
    from scipy.interpolate import make_interp_spline
    HAS_SCIPY = True
except Exception:
    HAS_SCIPY = False


def _curva_suave_fluida(ax, xs, ys, lw=1.8, color="#5a4ea1"):
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)

    if len(xs) < 2:
        return

    if len(xs) >= 3 and HAS_SCIPY:
        grau = min(3, len(xs) - 1)
        x_dense = np.linspace(xs.min(), xs.max(), 400)
        spline = make_interp_spline(xs, ys, k=grau)
        y_dense = spline(x_dense)
        ax.plot(x_dense, y_dense, color=color, lw=lw, zorder=4)
    else:
        verts = [(xs[0], ys[0])]
        codes = [Path.MOVETO]
        for i in range(len(xs) - 1):
            x0, y0 = xs[i], ys[i]
            x1, y1 = xs[i + 1], ys[i + 1]
            dx = x1 - x0
            c1 = (x0 + dx * 0.35, y0)
            c2 = (x0 + dx * 0.65, y1)
            verts.extend([c1, c2, (x1, y1)])
            codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])
        patch = PathPatch(Path(verts, codes), fill=False, lw=lw, color=color)
        ax.add_patch(patch)


def gerar_grafico_pontos_compostos(
    valores,
    output_path="/mnt/data/grafico_pontos_compostos_linha_fluida.png",
    titulo="Perfil dos Pontos Compostos",
):
    colunas = ["ICV", "IOP", "IMO", "IVP", "QIT"]
    n = len(colunas)

    y_min = 40
    y_max = 160

    y_grid_bottom = 40
    y_grid_top = 160
    y_valores_bottom = 160
    y_valores_top = 163.8
    y_siglas_bottom = 163.8
    y_siglas_top = 167.9

    fig, ax = plt.subplots(figsize=(7.1, 9.8), dpi=180)
    line_color = "black"

    ax.axhline(100, linewidth=1.0, color="#4c7a8b", zorder=0)

    ax.add_patch(Rectangle((0.5, y_grid_bottom), n, y_siglas_top - y_grid_bottom,
                           fill=False, lw=1.0, color=line_color))

    for y, lw in [
        (y_valores_bottom, 0.9),
        (y_valores_top, 0.9),
        (y_siglas_bottom, 0.9),
        (y_siglas_top, 0.9),
    ]:
        ax.plot([0.5, n + 0.5], [y, y], color=line_color, lw=lw)

    for x in np.arange(0.5, n + 1.5, 1):
        ax.plot([x, x], [y_grid_bottom, y_siglas_top], color=line_color, lw=0.9)

    for x in range(1, n + 1):
        for y in range(y_min, y_max + 1):
            if y % 10 == 0:
                half = 0.11
                lw = 0.8
            elif y % 5 == 0:
                half = 0.08
                lw = 0.7
            else:
                half = 0.045
                lw = 0.55
            ax.plot([x - half, x + half], [y, y], color="black", lw=lw, zorder=1)

    xs, ys = [], []
    for i, nome in enumerate(colunas, start=1):
        valor = valores.get(nome, "")
        ax.text(
            i, (y_siglas_bottom + y_siglas_top) / 2,
            nome, ha="center", va="center",
            fontsize=10.2, family="serif"
        )
        if valor != "" and valor is not None:
            ax.text(
                i, (y_valores_bottom + y_valores_top) / 2,
                str(valor), ha="center", va="center",
                fontsize=14, family="serif", color="#2f3e9e"
            )
        if isinstance(valor, (int, float)):
            xs.append(i)
            ys.append(valor)

    if len(xs) >= 2:
        _curva_suave_fluida(ax, xs, ys, lw=1.9, color="#5a4ea1")

    ax.plot(xs, ys, linestyle="None", marker="_", markersize=14, markeredgewidth=1.4,
            color="#5a4ea1", zorder=5)

    yticks = list(range(40, 161, 10))
    ax.set_yticks(yticks)
    ax.set_yticklabels([str(y) for y in yticks], fontsize=10, family="serif", color="dimgray")

    ax.set_xticks([])
    ax.set_xlim(0.35, n + 0.65)
    ax.set_ylim(38, 169.8)
    ax.set_title(titulo, fontsize=15, fontweight="bold", pad=10, family="serif")

    for side in ["top", "right", "bottom", "left"]:
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="y", length=0)

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    valores_exemplo = {
        "ICV": 123,
        "IOP": 110,
        "IMO": 98,
        "IVP": 101,
        "QIT": 113,
    }
    gerar_grafico_pontos_compostos(valores_exemplo)
