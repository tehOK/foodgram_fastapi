from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.crud import TagsCRUD
from core.models import db_helper
from core.schemas import TagRead


router = APIRouter(
    tags=["Теги"],
)

@router.get("/", response_model=list[TagRead])
async def read_tags(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    tags = await TagsCRUD.find_all(session=session)
    return tags

@router.get("/{tag_id}", response_model=TagRead)
async def read_tag_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    tag_id: int
):
    tag = await TagsCRUD.find_by_id(session=session, model_id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Тег не найден")
    return tag