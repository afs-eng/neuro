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

    lines = []
    lines.append("=" * 50)
    lines.append("RESULTADOS FDT")
    lines.append(f"Faixa etária: {faixa}")
    lines.append("=" * 50)
    lines.append("")

    if automatic:
        lines.append("PROCESSOS AUTOMÁTICOS")
        lines.append("-" * 30)
        for item in automatic:
            nome = item.get("nome", "")
            classificacao = item.get("classificacao", "-")
            pctl = item.get("percentil_num", 0)
            lines.append(f"  {nome}: {classificacao} (percentil {pctl})")
        lines.append("")

    if controlled:
        lines.append("PROCESSOS CONTROLADOS")
        lines.append("-" * 30)
        for item in controlled:
            nome = item.get("nome", "")
            classificacao = item.get("classificacao", "-")
            pctl = item.get("percentil_num", 0)
            lines.append(f"  {nome}: {classificacao} (percentil {pctl})")
        lines.append("")

    derived = merged_data.get("derived_scores", {})
    lines.append("ÍNDICES DERIVADOS")
    lines.append("-" * 30)
    lines.append(f"  Índice de Inibição: {derived.get('inibicao', 0)}")
    lines.append(f"  Índice de Flexibilidade: {derived.get('flexibilidade', 0)}")
    lines.append(f"  Total de Erros: {derived.get('total_erros', 0)}")

    return "\n".join(lines)
