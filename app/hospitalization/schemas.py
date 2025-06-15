from datetime import date

from pydantic import BaseModel

from app.doctors.schemas import SDoctor
from app.patients.schemas import SPatient


class SHospitalization(BaseModel):
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


class SHospitalizationFull(SHospitalization):
    patients: SPatient
    doctors: SDoctor


class SHospitalizationAdd(BaseModel):
    department: str
    purpose: str
    start_date: date
    end_date: date
    is_paid: bool
    room_id: int

    refusal_patient: bool | None
    refusal_doctor: bool | None
    cancel_reason: str | None
