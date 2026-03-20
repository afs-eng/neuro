from datetime import date
from typing import Optional

from ninja import Schema
from pydantic import EmailStr


class PatientOut(Schema):
    id: int
    full_name: str
    birth_date: Optional[date] = None
    sex: str
    schooling: str
    school_name: str
    occupation: str
    mother_name: str
    father_name: str
    phone: str
    email: str
    city: str
    state: str
    notes: str


class PatientCreateIn(Schema):
    full_name: str
    birth_date: Optional[date] = None
    sex: Optional[str] = ""
    schooling: Optional[str] = ""
    school_name: Optional[str] = ""
    occupation: Optional[str] = ""
    mother_name: Optional[str] = ""
    father_name: Optional[str] = ""
    phone: Optional[str] = ""
    email: Optional[EmailStr] = None
    city: Optional[str] = ""
    state: Optional[str] = ""
    notes: Optional[str] = ""


class PatientUpdateIn(Schema):
    full_name: Optional[str] = None
    birth_date: Optional[date] = None
    sex: Optional[str] = None
    schooling: Optional[str] = None
    school_name: Optional[str] = None
    occupation: Optional[str] = None
    mother_name: Optional[str] = None
    father_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    city: Optional[str] = None
    state: Optional[str] = None
    notes: Optional[str] = None


class MessageOut(Schema):
    message: str