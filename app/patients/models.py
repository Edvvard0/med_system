import uuid
from datetime import date, datetime
from enum import Enum

from sqlalchemy import text, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM as PgEnum, types

from app.database import Base


class CorrectGender(Enum):
    MAN: str = "man"
    WOMAN: str = "woman"


class Patient(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    middle_name: Mapped[str] = mapped_column(nullable=True)
    date_birthday: Mapped[date] = mapped_column(Date, nullable=False)

    passport: Mapped[str] = mapped_column(nullable=False)

    gender: Mapped[str] = mapped_column(
        PgEnum(CorrectGender, name="correct_gender_enum", create_type=False),
        nullable=False,
    )
    address: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)

    med_card_id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4,
    )
    photo_url: Mapped[str] = mapped_column(nullable=True)
    qr_code_url: Mapped[str] = mapped_column(nullable=True)

    date_issue: Mapped[date] = mapped_column(Date)
    date_last_request: Mapped[datetime] = mapped_column(Date)
    date_next_visit: Mapped[datetime] = mapped_column(Date)
    number_insurance_policy: Mapped[str]
    date_expiration: Mapped[date] = mapped_column(Date)
    diagnosis: Mapped[str]

    insurance_company: Mapped[str]

    password: Mapped[str]

    hospitalizations = relationship("Hospitalization", back_populates="patients")
    medprocedures = relationship("MedProcedure", back_populates="patients")
    room_patients = relationship("RoomPatients", back_populates="patients")
