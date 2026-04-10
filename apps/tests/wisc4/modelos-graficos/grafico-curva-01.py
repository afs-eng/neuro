import numpy as np
import matplotlib.pyplot as plt

def normal_pdf(x, media=100, dp=15):
    return (1 / (dp * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - media) / dp) ** 2)

def ler_int(msg):
    return int(float(input(msg).replace(",", ".")))

print("=== GERADOR DA CURVA NORMAL COM QI TOTAL ===")

qi_total = ler_int("QI Total: ")

nome_arquivo = input("\nDigite o nome do arquivo PNG (sem extensão): ").strip()
if not nome_arquivo:
    nome_arquivo = "curva_normal_qi_total"

media_normativa = 100
dp_normativo = 15

x = np.linspace(40, 160, 4000)
y_norma = normal_pdf(x, media_normativa, dp_normativo)

fig, ax = plt.subplots(figsize=(15, 8))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

faixas = [
    (40, 69, "#DDECEF", "Extremamente\nBaixo", "2,2%"),
    (70, 79, "#CFE3E8", "Limítrofe", "6,7%"),
    (80, 89, "#9FC9D2", "Média\nInferior", "16,1%"),
    (90, 109, "#F8FAF8", "Média", "50%"),
    (110, 119, "#9FC9D2", "Média\nSuperior", "16,1%"),
    (120, 129, "#CFE3E8", "Superior", "6,7%"),
    (130, 160, "#DDECEF", "Muito\nSuperior", "2,2%"),
]

for inicio, fim, cor, _, _ in faixas:
    mask = (x >= inicio) & (x <= fim)
    ax.fill_between(x[mask], y_norma[mask], 0, color=cor, zorder=1)

# Curva normativa completa
ax.plot(x, y_norma, color="black", linewidth=2.8, zorder=5)

# Linhas divisórias
divisoes = [70, 80, 90, 100, 110, 120, 130]
for v in divisoes:
    yv = normal_pdf(v, media_normativa, dp_normativo)
    ax.vlines(v, 0, yv, color="#555555", linewidth=1.0, zorder=2)

# Curva completa do QI Total
cor_qi = "#70AD47"
dp_qi = 15

y_qi = normal_pdf(x, media=qi_total, dp=dp_qi)
y_qi = y_qi / y_qi.max() * (y_norma.max() * 0.92)

ax.plot(
    x,
    y_qi,
    color=cor_qi,
    linewidth=2.8,
    alpha=0.98,
    zorder=6
)

# Barra vertical exatamente no valor do QI Total
topo_y_real = np.interp(qi_total, x, y_qi)
ax.vlines(
    qi_total,
    0,
    topo_y_real,
    color=cor_qi,
    linewidth=2.2,
    zorder=7
)

# Ponto e rótulo
ax.scatter(qi_total, topo_y_real, color=cor_qi, s=38, zorder=8)

ax.text(
    qi_total,
    topo_y_real + 0.0012,
    f"QI Total\n{qi_total}",
    ha="center",
    va="bottom",
    fontsize=10.5,
    color=cor_qi,
    fontweight="bold"
)

ax.text(
    100,
    y_norma.max() + 0.0015,
    "Curva normal",
    ha="center",
    va="bottom",
    fontsize=20,
    fontweight="bold",
    color="#333333"
)

# Tabela inferior
y_top = 0
y1 = -0.0032
y2 = -0.0062
y3 = -0.0092
y4 = -0.0118

for yy in [y_top, y1, y2, y3]:
    ax.hlines(yy, xmin=40, xmax=160, color="#444444", linewidth=1.5)

colunas = [40, 70, 80, 90, 110, 120, 130, 160]
for c in colunas:
    ax.vlines(c, y3, y_top, color="#444444", linewidth=1.5)

ax.text(28, (y_top + y1) / 2, "Porcentagem de casos", ha="right", va="center", fontsize=13)
ax.text(28, (y1 + y2) / 2, "Descrições Qualitativas", ha="right", va="center", fontsize=13)
ax.text(28, (y2 + y3) / 2, "Pontos Compostos", ha="right", va="center", fontsize=13)
ax.text(28, (y3 + y4) / 2, "Variação de Pontos Compostos", ha="right", va="center", fontsize=13)

centros = [
    (40 + 69) / 2,
    (70 + 79) / 2,
    (80 + 89) / 2,
    (90 + 109) / 2,
    (110 + 119) / 2,
    (120 + 129) / 2,
    (130 + 160) / 2,
]

for xc, faixa in zip(centros, faixas):
    _, _, _, descricao, porcentagem = faixa
    ax.text(xc, (y_top + y1) / 2, porcentagem, ha="center", va="center", fontsize=12)
    ax.text(xc, (y1 + y2) / 2, descricao, ha="center", va="center", fontsize=11.5)

pontos_ref = [70, 80, 90, 100, 110, 120, 130]
for p in pontos_ref:
    ax.text(p, (y2 + y3) / 2, str(p), ha="center", va="center", fontsize=12)

variacoes = ["≤ 69", "70–79", "80–89", "90–109", "110–119", "120–129", "≥ 130"]
for xc, txt in zip(centros, variacoes):
    ax.text(xc, (y3 + y4) / 2, txt, ha="center", va="center", fontsize=12)

ax.set_xlim(25, 160)
ax.set_ylim(-0.013, y_norma.max() + 0.012)
ax.set_xticks([])
ax.set_yticks([])

for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.savefig(f"{nome_arquivo}.png", dpi=300, bbox_inches="tight")
plt.show()

print(f"\nGráfico salvo com sucesso em: {nome_arquivo}.png")