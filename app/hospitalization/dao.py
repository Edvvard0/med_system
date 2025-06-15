import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.hospitalization.models import Hospitalization


class HospitalizationDAO(BaseDAO):
    model = Hospitalization

    @classmethod
    async def find_one_or_none_by_id(cls, session: AsyncSession, hosp_id: uuid.UUID):
        query = select(cls.model).filter_by(id=hosp_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_patient_by_hosp_id(
        cls, session: AsyncSession, hosp_id: uuid.UUID, options=None
    ):
        query = select(Hospitalization).filter_by(**{"id": hosp_id})
        if options:
            query = query.options(*options)
        rez = await session.execute(query)
        otv = rez.scalar_one_or_none()
        return otv

    @classmethod
    async def find_all_hosp(cls, session: AsyncSession, options=None):
        query = select(Hospitalization)
        if options:
            query = query.options(*options)
        rez = await session.execute(query)
        otv = rez.scalars().all()
        return otv
