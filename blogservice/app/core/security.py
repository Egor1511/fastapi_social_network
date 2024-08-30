import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.core.config.app_config import settings
from app.core.exceptions import (
    ForbiddenException,
    NoJwtException,
    NoUserIdException,
    TokenExpiredException,
    TokenNotFound,
)
from app.models.user_model import User
from app.services.user_service import user_service

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encode_jwt


async def authenticate_user(email: EmailStr, password: str) -> Optional[User]:
    user = await user_service.find_one(email=email)
    if not user or not verify_password(plain_password=password, hashed_password=user.hashed_password):
        return None
    return user


def get_token(request: Request):
    token = request.cookies.get("access_token")
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        expire: str = payload.get("exp")
        expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
        current_time = datetime.now(timezone.utc)

        if expire_time < current_time:
            raise TokenExpiredException

        user_id: str = payload.get("sub")
        if not user_id:
            raise NoUserIdException
        user = await user_service.find_by_id(int(user_id))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user
    except JWTError:
        raise NoJwtException


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        return current_user
    raise ForbiddenException
