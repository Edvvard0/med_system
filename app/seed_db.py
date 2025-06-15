import uuid
import asyncio
from datetime import date, datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker
from app.doctors.models import Doctor
from app.hospitalization.models import Hospitalization
from app.location.models import RoomHospital
from app.med_procedure.models import Cabinet, MedProcedure
from app.patients.models import CorrectGender, Patient

# Текущая дата и время (15 июня 2025, 15:21 CEST, преобразовано в UTC)
current_datetime = datetime(2025, 6, 15, 15, 21, tzinfo=timezone.utc)


async def seed_data():
    async with async_session_maker() as session:
        try:
            # 👨‍⚕️ Доктора
            doctors = [
                Doctor(
                    first_name=f"Doctor{i}",
                    last_name="Lastname",
                    middle_name="Middlename",
                    specialty="Therapist",
                    email=f"doctor{i}@clinic.com",
                    password="hashed_password",
                )
                for i in range(5)
            ]
            session.add_all(doctors)
            await session.flush()

            # 🏥 Кабинеты
            cabinets = [
                Cabinet(number_cabinet=100 + i, name=f"Cabinet {100 + i}")
                for i in range(5)
            ]
            session.add_all(cabinets)
            await session.flush()

            # Получаем ID кабинетов после вставки
            cabinet_ids = [cabinet.id for cabinet in cabinets]

            # 🧍 Пациенты
            patients = [
                Patient(
                    first_name=f"Patient{i}",
                    last_name="Last",
                    middle_name="Middle",
                    date_birthday=date(1990 + i, 1, 1),
                    passport=f"1234 56789{i}",
                    gender=CorrectGender.MAN if i % 2 == 0 else CorrectGender.WOMAN,
                    address=f"Street {i}",
                    phone_number=f"+7999000000{i}",
                    email=f"patient{i}@mail.com",
                    med_card_id=uuid.uuid4(),
                    photo_url=None,
                    qr_code_url=None,
                    date_issue=(current_datetime - timedelta(days=400)).date(),
                    date_last_request=(current_datetime - timedelta(days=10)).replace(
                        tzinfo=None
                    ),
                    date_next_visit=(current_datetime + timedelta(days=10)).replace(
                        tzinfo=None
                    ),
                    number_insurance_policy=f"POLICY{i:06}",
                    date_expiration=(current_datetime + timedelta(days=365)).date(),
                    diagnosis="Diagnosis text",
                    insurance_company="InsureCorp",
                    password="hashed_password",
                )
                for i in range(5)
            ]
            session.add_all(patients)
            await session.flush()

            # 🚪 Палаты
            rooms = [
                RoomHospital(count_all_bed=5, count_free_bed=5 - i) for i in range(5)
            ]
            session.add_all(rooms)
            await session.flush()

            # 🏨 Госпитализации
            hospitalizations = [
                Hospitalization(
                    patient_id=patients[i].id,
                    doctor_id=doctors[i].id,
                    room_id=rooms[i].id,
                    department="Therapy",
                    purpose="Examination",
                    start_date=(current_datetime - timedelta(days=7)).date(),
                    end_date=(current_datetime + timedelta(days=3)).date(),
                    is_paid=bool(i % 2),
                    refusal_patient=False,
                    refusal_doctor=False,
                    cancel_reason=None,
                )
                for i in range(5)
            ]
            session.add_all(hospitalizations)
            await session.flush()

            # 💉 Медпроцедуры
            medprocedures = [
                MedProcedure(
                    patient_id=patients[i].id,
                    doctor_id=doctors[i].id,
                    cabinet_id=cabinet_ids[
                        i
                    ],  # Используем id кабинета, а не number_cabinet
                    datetime_measures=current_datetime + timedelta(hours=i),
                    type_procedure="Checkup",
                    name_measures="ECG",
                    result="Normal",
                    recommendations="Rest well",
                    voice_comment=None,
                    file_med_procedure=None,
                )
                for i in range(5)
            ]
            session.add_all(medprocedures)

            await session.commit()
            print("Seed data successfully inserted!")

        except (SQLAlchemyError, Exception) as e:
            await session.rollback()
            print(f"Error occurred: {str(e)}")
            raise e


if __name__ == "__main__":
    asyncio.run(seed_data())
