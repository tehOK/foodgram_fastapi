from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.dependencies import get_auth_user
from core.models import db_helper
from core.schemas import UserRead

router = APIRouter(
    tags=["Подписки"],
)


@router.get("/subscriptions")
async def get_user_subsciptions(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: UserRead = Depends(get_auth_user),
):
    pass
