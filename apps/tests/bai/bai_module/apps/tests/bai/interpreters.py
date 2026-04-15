from __future__ import annotations


def build_bai_interpretation(computed_payload: dict, patient_name: str | None = None) -> str:
    name = patient_name or "O examinando"
    faixa = computed_payload["faixa_normativa"]
    interp = computed_payload["interpretacao_faixa"].lower()
    total = computed_payload["total_raw_score"]
    t_score = computed_payload.get("t_score")
    percentile = computed_payload.get("percentile")

    fragments = [
        f"{name} apresentou escore bruto total de {total} no Inventário de Ansiedade de Beck (BAI), "
        f"classificado na faixa {faixa.lower()}, compatível com {interp}."
    ]

    if t_score is not None:
        fragments.append(f" O escore T estimado foi {t_score:.0f}.")

    if percentile is not None:
        fragments.append(f" Esse desempenho corresponde aproximadamente ao percentil {percentile:.1f}.")

    fragments.append(
        " Em análise clínica, o resultado sugere intensidade ansiosa "
        "que deve ser interpretada em conjunto com a entrevista, observações comportamentais "
        "e demais instrumentos do protocolo avaliativo."
    )

    return "".join(fragments)
