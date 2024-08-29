from pydantic import BaseModel, EmailStr

from .base_schema import BaseSchema


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: str | None
    email: EmailStr | None
    password: str | None


class UserRead(BaseSchema):
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool
