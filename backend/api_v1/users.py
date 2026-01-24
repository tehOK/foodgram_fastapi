from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.crud import UsersCRUD
from api_v1.dependencies import get_auth_user
from core.models import User, db_helper
from core.schemas import (UserCreate, UserPasswordUpdate, UserRead,
                          UserSetAvatar)

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


@router.get("/subscriptions", response_model=list[UserRead])
async def get_user_subsciptions(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: User = Depends(get_auth_user),
):
    subsciptions = await UsersCRUD.get_user_subscribers(session=session, user=user)
    return subsciptions


@router.post("/set_password", status_code=status.HTTP_204_NO_CONTENT)
async def password_change(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    password_data: UserPasswordUpdate,
    user: UserRead = Depends(get_auth_user),
):
    await UsersCRUD.change_password(
        session=session, password_data=password_data, user=user
    )
    return


@router.get("/me", response_model=UserRead)
async def auth_user_info(user: User = Depends(get_auth_user)):
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
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id: int,
):
    user = await UsersCRUD.find_by_id(session=session, model_id=user_id)
    return user


@router.post("/{user_id}/subscribe", response_model=UserRead)
async def subscribe_on_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id: int,
    user: UserRead = Depends(get_auth_user),
):
    author = await UsersCRUD.create_subscibe_on_user(
        session=session, user_id=user_id, user=user
    )
    return author


@router.delete("/{user_id}/subscribe")
async def unsibscribe_author(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id: int,
    user: UserRead = Depends(get_auth_user),
):
    await UsersCRUD.delete_subscribe_on_author(
        session=session, user_id=user_id, user=user
    )
    return {"message": "success"}
