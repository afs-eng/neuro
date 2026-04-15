from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Optional

# Cache para evitar releitura do CSV
_t_score_table: Optional[List[dict]] = None


def _load_t_score_table() -> List[dict]:
    """Carrega a tabela normativa do BAI a partir do CSV."""
    global _t_score_table
    if _t_score_table is not None:
        return _t_score_table

    norms_dir = Path(__file__).parent.parent.parent / "norms" / "bai"
    csv_path = norms_dir / "t_score_lookup.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Tabela normativa do BAI não encontrada em {csv_path}")

    _t_score_table = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            _t_score_table.append(
                {
                    "raw_score_min": int(row["raw_score_min"]),
                    "raw_score_max": int(row["raw_score_max"]),
                    "t_score": int(row["t_score"]),
                }
            )

    return _t_score_table


def lookup_t_score(raw_score: int) -> Optional[int]:
    """
    Retorna o escore T normativo para um dado escore bruto do BAI.

    Usa a tabela oficial de normas (Amostra Geral, 18-90 anos).
    """
    table = _load_t_score_table()
    for entry in table:
        if entry["raw_score_min"] <= raw_score <= entry["raw_score_max"]:
            return entry["t_score"]
    return None


def get_norms_metadata() -> Dict[str, object]:
    """Retorna metadados da tabela normativa."""
    return {
        "instrument": "BAI",
        "scale": "Amostra Geral (T)",
        "dimension": "Escore Total",
        "age_range": "18-90",
        "fidedignidade": 0.90,
        "reliability": 0.90,
        "total_entries": len(_load_t_score_table()),
    }
