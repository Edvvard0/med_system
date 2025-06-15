from datetime import datetime

from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class MedProcedure(Base):
    __tablename__ = "med_procedures"

    patient_id: Mapped[int] = mapped_column(Integer, ForeignKey("patients.id"))
    doctor_id: Mapped[int] = mapped_column(Integer, ForeignKey("doctors.id"))
    cabinet_id: Mapped[int] = mapped_column(Integer, ForeignKey("cabinets.id"))

    datetime_measures: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    type_procedure: Mapped[str]
    name_measures: Mapped[str]
    result: Mapped[str]
    recommendations: Mapped[str]

    voice_comment: Mapped[str] = mapped_column(nullable=True)
    file_med_procedure: Mapped[str] = mapped_column(nullable=True)

    patients = relationship("Patient", back_populates="medprocedures")
    doctors = relationship("Doctor", back_populates="medprocedures")
    cabinet = relationship("Cabinet", back_populates="medprocedures")


class Cabinet(Base):
    number_cabinet: Mapped[int]
    name: Mapped[str]

    medprocedures = relationship("MedProcedure", back_populates="cabinet")
