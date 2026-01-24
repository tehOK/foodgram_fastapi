from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from api_v1.crud import BaseCRUD
from core.models import (Recipe, RecipeIngredientsAssociation,
                         RecipeTagsAssociation)


class RecipesCRUD(BaseCRUD):
    model = Recipe


    @classmethod
    async def get_all_recipes(cls, session: AsyncSession):

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
        print(query)
        recipes = await session.scalars(query)
        return list(recipes)
    
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
    