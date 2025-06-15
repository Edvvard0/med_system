import uuid
from datetime import date

from sqlalchemy import Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Hospitalization(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )  # это и будет индивидуальный код госпитализации, его вводить не надо

    patient_id: Mapped[int] = mapped_column(Integer, ForeignKey("patients.id"))
    doctor_id: Mapped[int] = mapped_column(Integer, ForeignKey("doctors.id"))
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey("roomhospitals.id"))

    department: Mapped[str]  # отделение
    purpose: Mapped[str]  # цель госпитализации
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    is_paid: Mapped[bool]  # True платно/ False бюджетно

    refusal_patient: Mapped[bool] = mapped_column(nullable=True, default=False)
    refusal_doctor: Mapped[bool] = mapped_column(nullable=True, default=False)
    cancel_reason: Mapped[str] = mapped_column(nullable=True)

    patients = relationship("Patient", back_populates="hospitalizations")
    doctors = relationship("Doctor", back_populates="hospitalizations")
