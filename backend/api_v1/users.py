from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.crud import UsersCRUD
from api_v1.dependencies import get_auth_user
from core.models import db_helper, User
from core.schemas import UserCreate, UserRead


router = APIRouter(
    tags=["Пользователи"]
)


@router.get("/", response_model=list[UserRead])
async def get_all_users(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
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

@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id: int
):
    user = await UsersCRUD.find_by_id(session=session, model_id=user_id)
    return user


@router.get("/me", response_model=UserRead)
async def auth_user_info(user: UserRead = Depends(get_auth_user)):
    return user