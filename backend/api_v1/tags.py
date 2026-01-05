from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.crud import TagsCRUD
from core.models import db_helper
from core.schemas import TagRead


router = APIRouter(
    tags=["Теги"],
)

@router.get("/tags/", response_model=list[TagRead])
async def read_tags(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    tags = await TagsCRUD.find_all(session=session)
    if not tags:
        raise HTTPException(status_code=404, detail="No tags found")
    return tags