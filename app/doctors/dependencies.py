from datetime import datetime

from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError

from app.config import settings
from app.database import SessionDep
from app.exception import (
    IncorrectFormatTokenException,
    TokenExpireException,
    NoPermissionsException,
    UserIsNotPresentException,
    NoTokenException,
)
from app.doctors.dao import DoctorDAO


def get_token(request: Request):
    token = request.cookies.get("access_token_doc")
    if not token:
        raise NoTokenException
    return token


async def get_current_user(session: SessionDep, token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise IncorrectFormatTokenException

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpireException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    user = await DoctorDAO.find_one_or_none_by_id(session, int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user


async def get_current_user_optional(request: Request, session: SessionDep):
    token = request.cookies.get("access_token_doc")

    if not token:
        return None
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        expire: str = payload.get("exp")
        if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
            return None
        user_id: str = payload.get("sub")
        if not user_id:
            return None
        user = await DoctorDAO.find_one_or_none_by_id(session, int(user_id))
        if not user:
            return None
        return user
    except JWTError:
        return None
