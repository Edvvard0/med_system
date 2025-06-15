from sqlalchemy import select, update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from app.dao.base import BaseDAO
from app.location.models import RoomHospital, RoomPatients


class RoomHospitalDAO(BaseDAO):
    model = RoomHospital

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        query = select(RoomHospital).where(RoomHospital.id == values["room_id"])
        result = await session.execute(query)
        room = result.scalar_one_or_none()

        if room.count_free_bed == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="нет свободных коек в этой палате",
            )

        new_instance = RoomPatients(
            room_hosp_id=room.id, patient_id=values["patient_id"]
        )
        session.add(new_instance)

        room.count_free_bed -= 1

        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return room

    @classmethod
    async def delete(cls, session: AsyncSession, **values):
        query = select(RoomHospital).where(RoomHospital.id == values["room_id"])
        result = await session.execute(query)
        room = result.scalar_one_or_none()

        if room.count_free_bed == room.count_all_bed:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="в палате никого нет"
            )

        room.count_free_bed += 1

        query = sqlalchemy_delete(RoomPatients).where(
            RoomPatients.room_hosp_id == values["room_id"],
            RoomPatients.patient_id == values["patient_id"],
        )
        await session.execute(query)

        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return room
