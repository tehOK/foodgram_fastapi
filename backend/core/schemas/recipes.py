from datetime import datetime
from typing import Annotated, List

from pydantic import BaseModel, BeforeValidator, ConfigDict

from .ingredients import IngredientForRecipe, IngredientInRecipe
from .tags import TagForRecipe, TagInRecipe


def get_tags_from_association_table(tags):
    return [
        TagInRecipe(
            id=tag.tag.id,
            name=tag.tag.name,
            slug=tag.tag.slug,
        )
        for tag in tags
    ]


def get_ingredients_from_association_table(ingredients):
    return [
        IngredientInRecipe(
            id=ingredient.ingredient.id,
            name=ingredient.ingredient.name,
            measurement_unit=ingredient.ingredient.measurement_unit,
            amount=ingredient.amount,
        )
        for ingredient in ingredients
    ]


class RecipeBase(BaseModel):
    id: int
    author: int
    name: str
    cooking_time: int
    text: str
    pub_date: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class RecipeRead(RecipeBase):
    id: int
    name: str
    text: str
    cooking_time: int
    pub_date: datetime
    tags: Annotated[List[TagInRecipe], BeforeValidator(get_tags_from_association_table)]
    ingredients: Annotated[
        List[IngredientInRecipe],
        BeforeValidator(get_ingredients_from_association_table),
    ]

    model_config = ConfigDict(
        from_attributes=True,
    )


class RecipeCreate(BaseModel):
    name: str
    text: str
    cooking_time: int
    ingredients: list[IngredientForRecipe]
    tags: list[TagForRecipe]
