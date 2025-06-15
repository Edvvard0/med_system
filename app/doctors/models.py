from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Doctor(Base):
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    middle_name: Mapped[str] = mapped_column(nullable=False)
    specialty: Mapped[str]

    email: Mapped[str]
    password: Mapped[str]

    hospitalizations = relationship("Hospitalization", back_populates="doctors")
    medprocedures = relationship("MedProcedure", back_populates="doctors")
