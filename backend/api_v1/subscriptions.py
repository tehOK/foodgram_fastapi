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


router = APIRouter(
    tags=["Подписки"],
)

@router.get("/subscriptions")
async def get_user_subsciptions(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user: UserRead = Depends(get_auth_user),
):
    pass