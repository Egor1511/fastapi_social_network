import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import (
    authenticate_user,
    create_access_token,
    get_current_admin_user,
    get_current_user,
    get_password_hash,
)
from app.models.schemas.user_schema import Token, UserCreate, UserRead, UserUpdate
from app.services.user_service import user_service

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate):
    existing_user = await user_service.get_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.hashed_password = get_password_hash(user.hashed_password)
    return await user_service.create(user)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, current_user: UserRead = Depends(get_current_user)):
    user = await user_service.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserUpdate, current_user: UserRead = Depends(get_current_user)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    updated_rows = await user_service.update(user, id=user_id)
    if not updated_rows:
        raise HTTPException(status_code=404, detail="User not found")
    return await user_service.find_by_id(user_id)


@router.post("/create_admin", response_model=UserRead)
async def create_admin(user: UserCreate):
    existing_user = await user_service.get_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.hashed_password = get_password_hash(user.hashed_password)
    user.is_admin = True
    return await user_service.create(user)


@router.delete("/{user_id}")
async def delete_user(user_id: int, current_user: UserRead = Depends(get_current_user)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    deleted_rows = await user_service.delete(id=user_id)
    if not deleted_rows:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}


@router.get("/", response_model=List[UserRead])
async def get_all_users(current_user: UserRead = Depends(get_current_user)):
    users = await user_service.get_all()
    logging.info(users)
    return users


@router.post("/make_admin/{user_id}")
async def make_user_admin(user_id: int, current_user: UserRead = Depends(get_current_admin_user)):
    user = await user_service.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_update = UserUpdate(is_admin=True)
    await user_service.update(user_update, id=user_id)
    return {"detail": "User is now an admin"}
