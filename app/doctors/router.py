from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from starlette.responses import Response

from app.database import SessionDep, async_session_maker
from app.doctors.auth import get_password_hash, authenticate_user, create_access_token
from app.doctors.dao import DoctorDAO
from app.doctors.dependencies import get_current_user
from app.doctors.schemas import SDoctor, SDoctorAdd, SDoctorAuth
from app.exception import IncorrectEmailOrPasswordException

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.get("/")
async def get_all_doctors(session: SessionDep) -> list[SDoctor]:
    doctors = await DoctorDAO.find_all(session)
    return doctors


@router.post("/")
async def add_doctors(session: SessionDep, data_doctor: SDoctorAdd):
    doctor = await DoctorDAO.find_one_or_none(session=session, email=data_doctor.email)
    if doctor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
        )

    hashed_password = get_password_hash(data_doctor.password)
    data_doctor.password = hashed_password

    async with async_session_maker() as session:
        await DoctorDAO.add(session, **data_doctor.model_dump())
    return {"message": "Доктор успешно зарегистрирован"}


@router.post("/login")
async def login_doctor(
    response: Response, doctor_data: SDoctorAuth, session: SessionDep
):
    patient = await authenticate_user(doctor_data.email, doctor_data.password, session)
    if not patient:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(patient.id)})
    response.set_cookie("access_token_doc", access_token, httponly=True)
    return access_token


@router.get("/me")
async def get_me_doc(doctor=Depends(get_current_user)) -> SDoctor:
    return doctor


@router.get("/{doctor_id}")
async def get_current_doctor(session: SessionDep, doctor_id: int) -> SDoctor | None:
    doctor = await DoctorDAO.find_one_or_none_by_id(session, model_id=doctor_id)
    return doctor
