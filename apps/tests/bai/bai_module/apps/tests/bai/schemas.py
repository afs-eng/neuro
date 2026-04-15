from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(slots=True)
class BAIItemResponse:
    item_number: int
    score: int


@dataclass(slots=True)
class BAIRawPayload:
    respondent_name: Optional[str] = None
    application_mode: str = "paper"
    responses: List[BAIItemResponse] = field(default_factory=list)


@dataclass(slots=True)
class BAIComputedPayload:
    total_raw_score: int
    t_score: Optional[float]
    percentile: Optional[float]
    confidence_interval: Optional[List[float]]
    missing_count: int
    faixa_normativa: str
    interpretacao_faixa: str
    response_distribution: Dict[int, int]
    tables: Dict[str, list]
    chart_payload: Dict[str, object]
