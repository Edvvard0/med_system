import uuid
from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict, field_validator

from app.patients.models import CorrectGender


class SPatientAdd(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    date_birthday: date
    passport: str
    gender: CorrectGender
    address: str
    phone_number: str
    email: EmailStr

    date_issue: date
    date_last_request: datetime
    date_next_visit: datetime
    number_insurance_policy: str
    date_expiration: date
    diagnosis: str

    insurance_company: str
    password: str

    @field_validator("date_last_request", "date_next_visit", mode="before")
    @classmethod
    def remove_timezone(cls, v: datetime) -> datetime:
        if isinstance(v, datetime) and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v

    model_config = ConfigDict(from_attributes=True)


class SPatient(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str
    date_birthday: date
    gender: CorrectGender
    address: str
    phone_number: str
    email: EmailStr

    date_issue: date
    date_last_request: datetime
    date_next_visit: datetime
    number_insurance_policy: str
    date_expiration: date
    diagnosis: str

    photo_url: str | None
    qr_code_url: str | None

    insurance_company: str

    model_config = ConfigDict(from_attributes=True)


class SPatientAuth(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class SHosp(BaseModel):
    patient_id: int
    doctor_id: int

    department: str
    purpose: str
    start_date: date
    end_date: date
    is_paid: bool

    refusal_patient: bool | None
    refusal_doctor: bool | None
    cancel_reason: str | None


class SPatientHosp(SPatient):
    hospitalizations: list[SHosp]
