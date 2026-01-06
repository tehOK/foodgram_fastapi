from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from api_v1.crud import UsersCRUD, TagsCRUD, RecipesCRUD
from core.models import db_helper, User, Recipe, RecipeIngredientsAssociation, RecipeTagsAssociation
from core.schemas import RecipeRead, RecipeCreate

from pydantic import ValidationError


router = APIRouter(
    tags=["Рецепты"]
)

@router.get("/", response_model=list[RecipeRead], description="Получить все рецепты")
async def get_all_recipes(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    recipes = await RecipesCRUD.get_all_recipes(session=session)
    return recipes

@router.post("/", response_model=RecipeRead)
async def create_recipe(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    recipe_data: RecipeCreate
):
    try:
        async with session.begin():
            new_recipe = Recipe(
                author=1,
                name=recipe_data.name,
                text=recipe_data.text,
                cooking_time=recipe_data.cooking_time
            )
            session.add(new_recipe)
            await session.flush()

            for tag_data in recipe_data.tags:
                recipe_with_tag = RecipeTagsAssociation(
                    recipe_id=new_recipe.id,
                    tag_id=tag_data.id
                )
                session.add(recipe_with_tag)

            for igredient_data in recipe_data.ingredients:
                recipe_with_ing = RecipeIngredientsAssociation(
                    recipe_id=new_recipe.id,
                    ingredient_id=igredient_data.id,
                    amount=igredient_data.amount
                )
                session.add(recipe_with_ing)

            await session.commit()
    except ValidationError as e:
        raise HTTPException(status_code=422, detail='111')
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании рецепта, {e}")
    
    recipe = await RecipesCRUD.find_recipe_by_id(session=session, recipe_id=new_recipe.id)

    return recipe