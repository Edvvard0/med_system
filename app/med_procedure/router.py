from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import selectinload
from starlette.responses import FileResponse

from app.database import SessionDep
from app.doctors.dependencies import get_current_user
from app.med_procedure.dao import MedProcedureDAO, CabinetDAO
from app.med_procedure.models import MedProcedure
from app.med_procedure.schemas import SCabinet, SMedProcedureAdd, SMedProcedureFull

router = APIRouter(prefix="/med_procedure", tags=["med_procedure"])


@router.get("/")
async def get_all_med_procedure(session: SessionDep):
    rez = await MedProcedureDAO.find_all_med_procedures(
        session,
        options=[
            selectinload(MedProcedure.patients),
            selectinload(MedProcedure.doctors),
            selectinload(MedProcedure.cabinet),
        ],
    )
    return rez


@router.get("/patient/{patient_id}")
async def get_all_med_procedure_by_current_patient(
    session: SessionDep, patient_id: int
) -> list[SMedProcedureFull]:
    rez = await MedProcedureDAO.find_all_med_procedures_current_patient(
        session,
        patient_id=patient_id,
        options=[
            selectinload(MedProcedure.patients),
            selectinload(MedProcedure.doctors),
            selectinload(MedProcedure.cabinet),
        ],
    )
    return rez


@router.get("/patient_info/{patient_id}")
async def med_procedure_by_current_patient(session: SessionDep, patient_id: int):
    rez = await MedProcedureDAO.find_all_med_procedures_current_patient(
        session, patient_id=patient_id
    )
    return rez


@router.post("/patient/{patient_id}")
async def add_med_procedure(
    session: SessionDep,
    patient_id: int,
    med_procedure_data: SMedProcedureAdd,
    doctor=Depends(get_current_user),
):
    data = med_procedure_data.model_dump()
    data["patient_id"] = patient_id
    data["doctor_id"] = doctor.id
    data["type_procedure"] = med_procedure_data.type_procedure.value

    await MedProcedureDAO.add(session, **data)
    return {"message": "МедПроцедура успешно добавлена"}


@router.get("/cabinets")
async def get_all_cabinets(session: SessionDep) -> list[SCabinet]:
    cabinets = await CabinetDAO.find_all(session)
    return cabinets


@router.get("/{med_procedures_id}")
async def get_med_procedures(session: SessionDep, med_procedures_id: int):
    rez = await MedProcedureDAO.find_med_procedures(
        session,
        med_procedures_id,
        options=[
            selectinload(MedProcedure.patients),
            selectinload(MedProcedure.doctors),
            selectinload(MedProcedure.cabinet),
        ],
    )
    return rez


@router.post("/upload_file/{med_procedure_id}")
async def upload_file_med_procedure(
    uploaded_file: UploadFile,
    session: SessionDep,
    med_procedure=Depends(get_med_procedures),
):
    file = uploaded_file.file
    file_name = f"app/static/med_procedure_files/file_{str(med_procedure.id)}.docx"
    with open(file_name, "wb") as f:
        f.write(file.read())

    med_procedure.file_med_procedure = file_name

    await session.commit()
    return file_name


@router.post("/upload_voice_comments/{med_procedure_id}")
async def upload_voice_comments(
    uploaded_file: UploadFile,
    session: SessionDep,
    med_procedure=Depends(get_med_procedures),
):
    file = uploaded_file.file
    file_name = f"app/static/voice_comment/voice_{str(med_procedure.id)}.mp3"
    with open(file_name, "wb") as f:
        f.write(file.read())

    med_procedure.voice_comment = file_name

    await session.commit()
    return file_name


@router.get("/voice_comments/{med_procedure_id}")
async def get_voice_message(med_procedure_id: int):
    file_path = f"app/static/voice_comment/voice_{str(med_procedure_id)}.mp3"
    return FileResponse(
        path=file_path, filename="voice_comment.mp3", media_type="audio/mp3"
    )


@router.get("/file/{med_procedure_id}")
async def get_voice_message(med_procedure_id: int):
    file_path = f"app/static/med_procedure_files/file_{str(med_procedure_id)}.docx"

    return FileResponse(
        path=file_path,
        filename="med_procedure_file.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
