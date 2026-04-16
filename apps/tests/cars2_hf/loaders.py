from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def load_cars2_hf_norms() -> list[dict]:
    path = (
        Path(__file__).resolve().parent.parent
        / "norms"
        / "cars2_hf"
        / "raw_to_tscore.csv"
    )

    rows: list[dict] = []
    with path.open(newline="", encoding="utf-8") as file_handle:
        reader = csv.DictReader(file_handle)
        for row in reader:
            rows.append(
                {
                    "raw_min": float(row["raw_min"]),
                    "raw_max": float(row["raw_max"]),
                    "t_score": int(row["t_score"]),
                    "percentile": row["percentile"],
                }
            )

    return rows
