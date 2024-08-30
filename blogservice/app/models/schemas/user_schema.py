from pydantic import BaseModel, EmailStr

from .base_schema import BaseSchema


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool | None = True
    is_admin: bool | None = False


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    hashed_password: str | None = None
    is_active: bool | None = None
    is_admin: bool | None = None


class UserRead(BaseSchema):
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool
    is_admin: bool


class UserLogin(BaseModel):
    email: EmailStr
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
