from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from api_v1.crud import BaseCRUD
from core.models import (Recipe, RecipeIngredientsAssociation,
                         RecipeTagsAssociation)
from core.schemas import RecipeRead


class RecipesCRUD(BaseCRUD):
    model = Recipe


    @classmethod
    async def get_all_recipes(cls, session: AsyncSession) -> Page[RecipeRead]:

        query = (
            select(Recipe)
            #.options(joinedload(Recipe.author.user.name))
            #.options(selectinload(Recipe.tags).joinedload(RecipeTagsAssociation.tag))
            .options(selectinload(cls.model.tags).joinedload(
                RecipeTagsAssociation.tag))
            .options(
                selectinload(Recipe.ingredients).joinedload(
                    RecipeIngredientsAssociation.ingredient
                )
            )
        )
        recipes = await paginate(session, query=query)
        return recipes
    
    @classmethod
    async def find_recipe_by_id(cls, session: AsyncSession, recipe_id: int):
        query = (
            select(Recipe).filter_by(id=recipe_id)
            .options(selectinload(cls.model.tags).joinedload(
                RecipeTagsAssociation.tag))
            .options(
                selectinload(Recipe.ingredients).joinedload(
                    RecipeIngredientsAssociation.ingredient
                )
            )
        )
        recipes = await session.scalars(query)
        return recipes.one_or_none()
    