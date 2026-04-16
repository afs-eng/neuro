from pydantic import BaseModel


class CARS2HFItemInput(BaseModel):
    score: float
    observations: str = ""


class CARS2HFInput(BaseModel):
    patient_name: str | None = None
    evaluation_date: str | None = None
    examiner_name: str | None = None
    birth_date: str | None = None
    age_years: int | None = None
    age_months: int | None = None
    informant: str | None = None
    items: dict[str, CARS2HFItemInput]
