from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def load_scoring_rules() -> dict:
    path = (
        Path(__file__).resolve().parent.parent
        / "norms"
        / "mchat"
        / "scoring_rules.json"
    )

    with path.open(encoding="utf-8") as file_handle:
        return json.load(file_handle)
