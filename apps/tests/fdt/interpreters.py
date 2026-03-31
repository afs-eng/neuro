def interpret_fdt_result(merged_data: dict) -> str:
    metric_results = merged_data.get("metric_results", [])
    faixa = merged_data.get("faixa", "")

    automatic = [
        item
        for item in metric_results
        if item.get("categoria") == "Processos Automaticos"
    ]
    controlled = [
        item
        for item in metric_results
        if item.get("categoria") == "Processos Controlados"
    ]

    automatic_summary = ", ".join(
        f"{item['nome']}: {item['classificacao']} (pctl {item['percentil_num']})"
        for item in automatic
    )
    controlled_summary = ", ".join(
        f"{item['nome']}: {item['classificacao']} (pctl {item['percentil_num']})"
        for item in controlled
    )

    derived = merged_data.get("derived_scores", {})

    parts = [
        f"Faixa normativa utilizada: {faixa}.",
        f"Processos automaticos: {automatic_summary or 'Sem dados.'}",
        f"Processos controlados: {controlled_summary or 'Sem dados.'}",
        (
            "Indices derivados: "
            f"Inibicao = {derived.get('inibicao', 0)}, "
            f"Flexibilidade = {derived.get('flexibilidade', 0)}, "
            f"Erros totais = {derived.get('total_erros', 0)}."
        ),
    ]
    return "\n".join(parts)
