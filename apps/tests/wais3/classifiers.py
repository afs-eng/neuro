from __future__ import annotations


def classify_wais3_payload(computed_data: dict) -> dict:
    """Return the computed payload augmented with automatic GAI/CPI when possible.

    This function is conservative: it preserves the original computed_data
    structure and only adds 'gai_data' and 'cpi_data' when it can compute them
    via WISC-IV equivalence tables. Import of the WISC lookup functions is
    done lazily and errors are swallowed to avoid causing a 500 in the API.
    """
    if not computed_data:
        return {}

    result = dict(computed_data)
    # preserve/extend warnings
    warnings = list(result.get("warnings") or [])

    indices = result.get("indices") or {}

    def _safe_sum(keys: list[str]) -> int | None:
        s = 0
        found = False
        for k in keys:
            val = (indices.get(k) or {}).get("soma_ponderada")
            if val is not None:
                s += val
                found = True
        return s if found else None

    gai_soma = _safe_sum(["compreensao_verbal", "organizacao_perceptual"])
    cpi_soma = _safe_sum(["memoria_operacional", "velocidade_processamento"])

    gai_data = {"soma_ponderados": gai_soma, "escore_composto": None, "percentil": None, "intervalo_confianca": None, "classificacao": None}
    cpi_data = {"soma_ponderados": cpi_soma, "escore_composto": None, "percentil": None, "intervalo_confianca": None, "classificacao": None}

    # Lazy import to avoid import-time circular dependencies / errors
    try:
        from apps.tests.wisc4.calculators import lookup_gai_score, lookup_cpi_score
    except Exception:
        lookup_gai_score = None
        lookup_cpi_score = None

    if lookup_gai_score and gai_soma is not None:
        try:
            res = lookup_gai_score(gai_soma)
            # lookup returns keys: 'escore', 'percentil', 'ic_95', 'classificacao'
            gai_data.update({
                "escore_composto": res.get("escore"),
                "percentil": res.get("percentil"),
                "intervalo_confianca": res.get("ic_95") or res.get("ic_90") or None,
                "classificacao": res.get("classificacao"),
            })
        except Exception as exc:
            warnings.append(f"GAI lookup failed: {exc}")

    if lookup_cpi_score and cpi_soma is not None:
        try:
            res = lookup_cpi_score(cpi_soma)
            cpi_data.update({
                "escore_composto": res.get("escore"),
                "percentil": res.get("percentil"),
                "intervalo_confianca": res.get("ic_95") or res.get("ic_90") or None,
                "classificacao": res.get("classificacao"),
            })
        except Exception as exc:
            warnings.append(f"CPI lookup failed: {exc}")

    result["gai_data"] = gai_data
    result["cpi_data"] = cpi_data
    if warnings:
        result["warnings"] = warnings

    return result
