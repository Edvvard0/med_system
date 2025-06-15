from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class SPersonLocations(BaseModel):
    PersonCode: str
    PersonRole: Literal["Клиент", "Сотрудник"]
    LastSecurityPointNumber: int
    LastSecurityPointDirection: Literal["in", "out"]
    LastSecurityPointTime: datetime


class SPersonCabinet(BaseModel):
    LastSecurityPointNumber: int
    CountDoctors: int | None = Field(default=0)
    CountPatients: int | None = Field(default=0)


class SRoomHospital(BaseModel):
    room_id: int
    count_all_bed: int
    count_free_bed: int
    patient_id: int


class SRoomHospitalAdd(BaseModel):
    room_id: int
    patient_id: int
