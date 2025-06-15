from app.dao.base import BaseDAO
from app.doctors.models import Doctor


class DoctorDAO(BaseDAO):
    model = Doctor
