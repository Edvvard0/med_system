from pydantic import BaseModel, EmailStr


class SDoctor(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    specialty: str

    email: EmailStr


class SDoctorAdd(SDoctor):
    password: str


class SDoctorAuth(BaseModel):
    email: EmailStr
    password: str
