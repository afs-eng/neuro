import os
import csv
from datetime import date, datetime


NORMS_DIR = os.path.join(os.path.dirname(__file__), "..", "norms", "tabelas_bpa2")

SUBTESTES_ENTRADA = {
    "concentrada": {"codigo": "ac", "nome": "Atenção Concentrada"},
    "dividida": {"codigo": "ad", "nome": "Atenção Dividida"},
    "alternada": {"codigo": "aa", "nome": "Atenção Alternada"},
}

FAIXAS_ETARIAS = [
    "6 anos",
    "7 anos",
    "8 anos",
    "9 anos",
    "10 anos",
    "11 anos",
    "12 anos",
    "13 anos",
    "14 anos",
    "15-17 anos",
    "18-20 anos",
    "21-30 anos",
    "31-40 anos",
    "41-50 anos",
    "51-60 anos",
    "61-70 anos",
    "71-80 anos",
    "81 anos ou mais",
]


def calcular_idade(data_nascimento: date, data_avaliacao: date) -> int:
    idade = data_avaliacao.year - data_nascimento.year
    if (data_avaliacao.month, data_avaliacao.day) < (
        data_nascimento.month,
        data_nascimento.day,
    ):
        idade -= 1
    return idade


def obter_faixa_etaria(idade: int) -> str:
    if idade < 6:
        raise ValueError("Idade mínima para o BPA-2 é 6 anos")
    if idade <= 14:
        return f"{idade} anos"
    if idade <= 17:
        return "15-17 anos"
    if idade <= 20:
        return "18-20 anos"
    if idade <= 30:
        return "21-30 anos"
    if idade <= 40:
        return "31-40 anos"
    if idade <= 50:
        return "41-50 anos"
    if idade <= 60:
        return "51-60 anos"
    if idade <= 70:
        return "61-70 anos"
    if idade <= 80:
        return "71-80 anos"
    return "81 anos ou mais"


def carregar_tabela(codigo: str, modo: str) -> list[dict]:
    suffix = "age" if modo == "1" else "escolaridade"
    filename = f"{codigo}_{suffix}.csv"
    filepath = os.path.join(NORMS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Tabela não encontrada: {filepath}")

    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader)


def classificar_escore(
    escore_total: int, tabela: list[dict], faixa: str
) -> tuple[str, int]:
    for row in tabela:
        valor = row.get(faixa)
        if valor is None:
            continue
        try:
            valor_int = int(valor)
        except ValueError:
            continue
        if escore_total <= valor_int:
            return row["classificação"], int(row["Percentil"])

    ultimo = tabela[-1]
    return ultimo["classificação"], int(ultimo["Percentil"])


def solicitar_dados_teste(nome_subteste: str) -> dict:
    print(f"\n--- {nome_subteste} ---")
    while True:
        try:
            brutos = int(input("  Pontos Brutos: "))
            erros = int(input("  Erros: "))
            omissoes = int(input("  Omissões: "))
            total = brutos - erros - omissoes
            print(f"  Total: {total}")
            return {
                "brutos": brutos,
                "erros": erros,
                "omissoes": omissoes,
                "total": total,
            }
        except ValueError:
            print("  Valor inválido. Digite números inteiros.")


def main():
    print("=" * 50)
    print("  BPA-2 - Bateria de Provas Neuropsicológicas")
    print("  de Atenção")
    print("=" * 50)

    print("\nEscolha o modo de normatização:")
    print("  1 - Idade")
    print("  2 - Escolaridade")
    modo = input("\nOpção (1 ou 2): ").strip()

    if modo not in ("1", "2"):
        print("Opção inválida.")
        return

    print("\n--- Dados do Paciente ---")
    nome = input("Nome do paciente: ").strip()

    while True:
        try:
            data_nasc_str = input("Data de nascimento (DD/MM/AAAA): ").strip()
            data_nasc = datetime.strptime(data_nasc_str, "%d/%m/%Y").date()
            break
        except ValueError:
            print("Data inválida. Use o formato DD/MM/AAAA.")

    while True:
        try:
            data_eval_str = input("Data da avaliação (DD/MM/AAAA): ").strip()
            data_eval = datetime.strptime(data_eval_str, "%d/%m/%Y").date()
            break
        except ValueError:
            print("Data inválida. Use o formato DD/MM/AAAA.")

    idade = calcular_idade(data_nasc, data_eval)
    print(f"\nIdade no momento da avaliação: {idade} anos")

    if modo == "1":
        try:
            faixa = obter_faixa_etaria(idade)
        except ValueError as e:
            print(f"Erro: {e}")
            return
        print(f"Faixa etária: {faixa}")
    else:
        print("\nEscolaridade:")
        print("  1 - 1 ano  2 - 2 anos  3 - 3 anos  4 - 4 anos")
        print("  5 - 5 anos  6 - 6 anos  7 - 7 anos  8 - 8 anos")
        print("  9 - 9 anos  10 - 10 anos  11 - 11 anos  12 - 12 anos")
        escolaridade = input("Anos de escolaridade: ").strip()
        faixa = f"{escolaridade} ano{'s' if escolaridade != '1' else ''}"

    print("\n" + "=" * 50)
    print("  PREENCHIMENTO DOS SUBTESTES")
    print("=" * 50)

    resultados = {}
    for key, info in SUBTESTES_ENTRADA.items():
        dados = solicitar_dados_teste(info["nome"])
        tabela = carregar_tabela(info["codigo"], modo)
        classificacao, percentil = classificar_escore(dados["total"], tabela, faixa)

        resultados[key] = {
            "nome": info["nome"],
            **dados,
            "classificacao": classificacao,
            "percentil": percentil,
        }

    total_geral = sum(r["total"] for r in resultados.values())
    bruto_geral = sum(r["brutos"] for r in resultados.values())
    erros_geral = sum(r["erros"] for r in resultados.values())
    omissoes_geral = sum(r["omissoes"] for r in resultados.values())
    tabela_geral = carregar_tabela("ag", modo)
    classif_geral, perc_geral = classificar_escore(total_geral, tabela_geral, faixa)

    resultados["geral"] = {
        "nome": "Atenção Geral",
        "brutos": bruto_geral,
        "erros": erros_geral,
        "omissoes": omissoes_geral,
        "total": total_geral,
        "classificacao": classif_geral,
        "percentil": perc_geral,
    }

    print("\n" + "=" * 50)
    print("  RESULTADOS")
    print("=" * 50)
    print(f"\nPaciente: {nome}")
    print(f"Idade: {idade} anos | Faixa: {faixa}")
    print(f"Data da avaliação: {data_eval.strftime('%d/%m/%Y')}")

    print(
        f"\n{'Subteste':<25} {'Bruto':>6} {'Erros':>6} {'Omis':>6} {'Total':>6} {'Classificação':<20} {'%il':>5}"
    )
    print("-" * 80)

    for key, r in resultados.items():
        print(
            f"{r['nome']:<25} {r['brutos']:>6} {r['erros']:>6} {r['omissoes']:>6} {r['total']:>6} {r['classificacao']:<20} {r['percentil']:>5}"
        )

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
