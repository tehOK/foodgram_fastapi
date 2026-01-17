from typing import Annotated
import base64
import uuid
import re
from pathlib import Path
from fastapi import HTTPException
#from PIL import Image
from io import BytesIO
from typing import Tuple, Optional
import imghdr

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.crud import UsersCRUD
from api_v1.dependencies import get_auth_user
from core.models import db_helper, User
from core.schemas import UserCreate, UserRead, UserPasswordUpdate, UserSetAvatar


router = APIRouter(tags=["Пользователи"])


@router.get("/", response_model=list[UserRead])
async def get_all_users(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    users = await UsersCRUD.find_all(session=session)
    return users


@router.post("/", response_model=UserRead)
async def create_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: UserCreate,
) -> User:
    try:
        user = await UsersCRUD.create_user(session=session, user=user)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/set_password", status_code=status.HTTP_204_NO_CONTENT)
async def password_change(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    password_data: UserPasswordUpdate,
    user: UserRead = Depends(get_auth_user),
):  
    await UsersCRUD.change_password(session=session, password_data=password_data, user=user)
    return


@router.get("/me", response_model=UserRead)
async def auth_user_info(user: UserRead = Depends(get_auth_user)):
    return user

@router.put("/me/avatar")
async def set_user_avatar(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    avatar: UserSetAvatar,
    user: UserRead = Depends(get_auth_user),
):
    print(avatar.avatar)
    print(user)
    pass
    

@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)], user_id: int
):
    user = await UsersCRUD.find_by_id(session=session, model_id=user_id)
    return user

