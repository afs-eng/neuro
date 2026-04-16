from pydantic import BaseModel


class MCHATResponseItem(BaseModel):
    answer: str


class MCHATInput(BaseModel):
    patient_name: str | None = None
    evaluation_date: str | None = None
    birth_date: str | None = None
    age_months: int | None = None
    respondent_name: str | None = None
    respondent_relationship: str | None = None
    items: dict[str, MCHATResponseItem]
