from apps.tests.bfp.interpreters import build_bfp_report_highlights


def test_build_bfp_report_highlights_empty():
    payload = {}
    out = build_bfp_report_highlights(payload)
    assert isinstance(out, dict)
    assert out.get("summary") == "Perfil sem alterações clinicamente salientes nos fatores principais."
    assert out.get("relevant") == []


def test_build_bfp_report_highlights_elevation_and_reduction():
    payload = {
        "factors": {
            "NN": {"percentile": 90, "classification": "Muito elevado"},
            "RR": {"percentile": 10, "classification": "Reduzido"},
            "EE": {"percentile": 50, "classification": "Média"},
            "SS": {"percentile": 40, "classification": "Média"},
            "AA": {"percentile": 55, "classification": "Média"},
        }
    }
    out = build_bfp_report_highlights(payload)
    assert "elevação" in out.get("summary") or "redução" in out.get("summary")
    assert any(item["code"] == "NN" for item in out.get("relevant"))
    assert any(item["code"] == "RR" for item in out.get("relevant"))
