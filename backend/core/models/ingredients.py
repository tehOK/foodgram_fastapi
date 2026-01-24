from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IdIntPkMixin

if TYPE_CHECKING:
    from .recipe_ingredients_association import RecipeIngredientsAssociation


class Ingredient(IdIntPkMixin, Base):
    name: Mapped[str] = mapped_column(String(128))
    measurement_unit: Mapped[str] = mapped_column(String(64))

    recipe: Mapped[list["RecipeIngredientsAssociation"]] = relationship(
        back_populates="ingredient",
    )
