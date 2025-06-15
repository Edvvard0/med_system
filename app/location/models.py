from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.database import Base


class RoomHospital(Base):
    count_all_bed: Mapped[int]
    count_free_bed: Mapped[int]

    room_patients = relationship("RoomPatients", back_populates="room_hosp")


class RoomPatients(Base):
    room_hosp_id: Mapped[int] = mapped_column(Integer, ForeignKey("roomhospitals.id"))
    patient_id: Mapped[int] = mapped_column(Integer, ForeignKey("patients.id"))

    room_hosp = relationship("RoomHospital", back_populates="room_patients")
    patients = relationship("Patient", back_populates="room_patients")
