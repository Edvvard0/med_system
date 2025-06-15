from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import selectinload
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.database import SessionDep
from app.location.dao import RoomHospitalDAO
from app.location.models import RoomHospital
from app.location.schemas import SRoomHospitalAdd
from app.location.utils import get_pearson_location

router = APIRouter(prefix="/location", tags=["Location"])

template = Jinja2Templates(directory="app/templates")


@router.get("/")
async def get_hosp_cabinet_page(
    request: Request, personal=Depends(get_pearson_location)
) -> HTMLResponse:
    return template.TemplateResponse(
        name="hospital_cabinets.html",
        context={"request": request, "personal": personal},
    )


@router.get("/rooms")
async def get_rooms(session: SessionDep):
    rooms = await RoomHospitalDAO.find_all(session)
    return rooms


@router.post("/rooms/patient")
async def add_patient_in_room(session: SessionDep, room_hosp: SRoomHospitalAdd):
    await RoomHospitalDAO.add(session, **room_hosp.model_dump())
    return {"message": "койка успешна привязана к пользователю"}


@router.delete("/rooms/patient")
async def add_patient_in_room(session: SessionDep, room_hosp: SRoomHospitalAdd):
    await RoomHospitalDAO.delete(session, **room_hosp.model_dump())
    return {"message": "койка освобождена"}
