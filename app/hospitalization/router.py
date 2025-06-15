import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import selectinload

from app.database import SessionDep
from app.doctors.dependencies import get_current_user
from app.hospitalization.dao import HospitalizationDAO
from app.hospitalization.models import Hospitalization
from app.hospitalization.schemas import (
    SHospitalization,
    SHospitalizationFull,
    SHospitalizationAdd,
)

router = APIRouter(prefix="/hospitalizations", tags=["hospitalizations"])


@router.get("/")
async def get_hospitalizations(session: SessionDep) -> list[SHospitalization]:
    hosp = await HospitalizationDAO.find_all(session)
    return hosp


@router.post("/patient/{patient_id}")
async def add_hospitalization(
    session: SessionDep,
    hosp: SHospitalizationAdd,
    patient_id: int,
    doctor=Depends(get_current_user),
):
    data = hosp.model_dump()
    data["patient_id"] = patient_id
    data["doctor_id"] = doctor.id

    await HospitalizationDAO.add(session, **data)
    return {"message": "Госпитализация успешно добавлена"}


@router.get("/patients")
async def get_lst_hosp_full_info(session: SessionDep) -> list[SHospitalizationFull]:
    rez = await HospitalizationDAO.find_all_hosp(
        session,
        options=[
            selectinload(Hospitalization.patients),
            selectinload(Hospitalization.doctors),
        ],
    )
    return rez


@router.get("/patients/{hosp_id}")
async def get_patients_hosp(session: SessionDep, hosp_id: str) -> SHospitalizationFull:
    hosp_id = uuid.UUID(hosp_id)
    rez = await HospitalizationDAO.find_patient_by_hosp_id(
        session=session,
        hosp_id=hosp_id,
        options=[
            selectinload(Hospitalization.patients),
            selectinload(Hospitalization.doctors),
        ],
    )
    return rez


@router.get("/{hosp_id}")
async def get_current_hosp(
    hosp_id: str, session: SessionDep
) -> SHospitalization | None:
    hosp_id = uuid.UUID(hosp_id)
    hosp = await HospitalizationDAO.find_one_or_none_by_id(session, hosp_id=hosp_id)
    return hosp
