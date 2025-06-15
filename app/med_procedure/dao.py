from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.med_procedure.models import MedProcedure, Cabinet


class MedProcedureDAO(BaseDAO):
    model = MedProcedure

    @classmethod
    async def find_med_procedures(
        cls, session: AsyncSession, med_procedures: int, options=None
    ):
        query = select(MedProcedure).filter_by(**{"id": med_procedures})
        if options:
            query = query.options(*options)
        rez = await session.execute(query)
        otv = rez.scalar_one_or_none()
        return otv

    @classmethod
    async def find_all_med_procedures(cls, session: AsyncSession, options=None):
        query = select(MedProcedure)
        if options:
            query = query.options(*options)
        rez = await session.execute(query)
        otv = rez.scalars().all()
        return otv

    @classmethod
    async def find_all_med_procedures_current_patient(
        cls, session: AsyncSession, patient_id: int, options=None
    ):
        query = (
            select(MedProcedure)
            .filter_by(patient_id=patient_id)
            .order_by(MedProcedure.datetime_measures)
        )
        if options:
            query = query.options(*options)
        rez = await session.execute(query)
        otv = rez.scalars().all()
        return otv


class CabinetDAO(BaseDAO):
    model = Cabinet
