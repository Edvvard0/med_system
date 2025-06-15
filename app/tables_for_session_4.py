# https://dbdiagram.io/d/670a4c8397a66db9a3bd34fa


import uuid
from datetime import date, datetime
from enum import Enum

from sqlalchemy import text, Integer, ForeignKey, Boolean, DateTime, Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from app.database import Base
from app.doctors.models import Doctor


# -------------------
#  Роли пользователей
# -------------------


class Administrator(Base):
    __tablename__ = "administrators"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    middle_name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)


class Registrar(Base):
    __tablename__ = "registrars"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    middle_name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)


# -------------------
#  Расписание
# -------------------


class ScheduleTemplate(Base):
    __tablename__ = "schedule_templates"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    pattern_type: Mapped[str] = mapped_column(String, nullable=False)
    # шаблон: "even_days", "odd_days", "first_last_day", и др.

    schedules = relationship("Schedule", back_populates="template")


class Schedule(Base):
    __tablename__ = "schedules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    doctor_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("doctors.id"), nullable=False
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    template_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("schedule_templates.id"), nullable=True
    )

    doctor = relationship("Doctor", back_populates="schedules")
    template = relationship("ScheduleTemplate", back_populates="schedules")
    appointments = relationship("Appointment", back_populates="schedule")
    change_logs = relationship("ScheduleChangeLog", back_populates="schedule")


class ScheduleChangeLog(Base):
    __tablename__ = "schedule_change_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    schedule_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("schedules.id"), nullable=False
    )
    changed_by_admin_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("administrators.id"), nullable=True
    )
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    change_description: Mapped[str] = mapped_column(String, nullable=False)

    schedule = relationship("Schedule", back_populates="change_logs")
    changed_by = relationship("Administrator")


class Appointment(Base):
    __tablename__ = "appointments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    schedule_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("schedules.id"), nullable=False
    )
    patient_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("patients.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String, nullable=False
    )  # planned/completed/cancelled
    notes: Mapped[str] = mapped_column(String, nullable=True)

    schedule = relationship("Schedule", back_populates="appointments")
    patient = relationship("Patient")


# -------------------
# Резервирование ресурсов (проект)
# -------------------


class ReservedResource(Base):
    __tablename__ = "reserved_resources"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    resource_type: Mapped[str] = mapped_column(
        String, nullable=False
    )  # "cabinet", "operation_room", etc.
    resource_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reserved_for: Mapped[str] = mapped_column(String, nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_by_admin_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("administrators.id"), nullable=True
    )

    created_by = relationship("Administrator")


# -------------------
# Связи в Doctor (дополняем существующую модель)
# -------------------

Doctor.schedules = relationship("Schedule", back_populates="doctor")
Doctor.hospitalizations = relationship("Hospitalization", back_populates="doctors")
Doctor.medprocedures = relationship("MedProcedure", back_populates="doctors")
