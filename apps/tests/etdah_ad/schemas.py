from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict
from .config import QUESTIONS, FACTOR_NAMES


class ETDAHADResponseItem(BaseModel):
    item_number: int
    question: str
    score: int = Field(ge=0, le=5)


class ETDAHADFactorResult(BaseModel):
    name: str
    raw_score: int
    mean: float
    percentile_text: str
    classification: str


class ETDAHADInput(BaseModel):
    patient_id: int
    examiner_id: int
    age: int = Field(ge=18, le=60)
    schooling: int = Field(ge=1, le=20)
    responses: Dict[int, int] = Field(
        description="Respostas dos 69 itens (1-69), valores de 0 a 5"
    )

    @field_validator("responses")
    @classmethod
    def validate_responses(cls, v: Dict[int, int]) -> Dict[int, int]:
        if len(v) != 69:
            raise ValueError(f"Deve conter exatamente 69 itens, got {len(v)}")

        for item_num, score in v.items():
            if item_num < 1 or item_num > 69:
                raise ValueError(f"Número de item inválido: {item_num}")
            if score < 0 or score > 5:
                raise ValueError(f"Item {item_num}: score deve estar entre 0 e 5")

        return v


class ETDAHADResponse(BaseModel):
    id: int
    patient_id: int
    examiner_id: int
    age: int
    schooling: int
    raw_scores: Dict[str, int]
    results: Dict[str, ETDAHADFactorResult]
    report: str

    class Config:
        from_attributes = True
