from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.crud import IngredientsCRUD
from core.models import db_helper
from core.schemas import IngredientRead


router = APIRouter(
    tags=["Ингредиенты"]
)

@router.get("/", response_model=list[IngredientRead])
async def get_all_tags(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    ingredients = await IngredientsCRUD.find_all(session=session)
    return ingredients

@router.get("/{ingredient_id}", response_model=IngredientRead)
async def get_ingredient_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    ingredient_id: int
):
    ingredient = await IngredientsCRUD.find_by_id(session=session, model_id=ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ингредиент не найден")
    return ingredient
