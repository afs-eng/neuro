from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict


class ETDAHPAISResponseItem(BaseModel):
    item_number: int
    question: str
    score: int = Field(ge=1, le=6)


class ETDAHPAISFactorResult(BaseModel):
    name: str
    raw_score: int
    mean: float
    std: float
    z_score: float
    points_scaled: float
    percentile_text: str
    percentile_guilmette: float
    classification: str
    classification_guilmette: str


class ETDAHPAISInput(BaseModel):
    patient_id: int
    examiner_id: int
    age: int = Field(ge=2, le=17)
    sex: str = Field(pattern="^(M|F)$")
    schooling: int = Field(ge=1, le=20)
    responses: Dict[int, int] = Field(
        description="Respostas dos 58 itens (1-58), valores de 1 a 6"
    )

    @field_validator("responses")
    @classmethod
    def validate_responses(cls, v: Dict[int, int]) -> Dict[int, int]:
        if len(v) != 58:
            raise ValueError(f"Deve conter exatamente 58 itens, got {len(v)}")

        for item_num, score in v.items():
            if item_num < 1 or item_num > 58:
                raise ValueError(f"Número de item inválido: {item_num}")
            if score < 1 or score > 6:
                raise ValueError(f"Item {item_num}: score deve estar entre 1 e 6")

        return v


class ETDAHPAISResponse(BaseModel):
    id: int
    patient_id: int
    examiner_id: int
    age: int
    sex: str
    schooling: int
    raw_scores: Dict[str, int]
    results: Dict[str, ETDAHPAISFactorResult]
    report: str

    class Config:
        from_attributes = True
