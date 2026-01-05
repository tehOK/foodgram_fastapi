from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING

from .base import Base

# if TYPE_CHECKING:
#     from .recipe_ingredients_association import RecipeIngredientsAssociation

class Ingredient(Base):
    name: Mapped[str] = mapped_column(String(128))
    measurement_unit: Mapped[str] = mapped_column(String(64))

    # recipe: Mapped[list["RecipeIngredientsAssociation"]] = relationship(
    #     back_populates="ingredient",
    # )