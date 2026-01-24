from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IdIntPkMixin

if TYPE_CHECKING:
    from .ingredients import Ingredient
    from .recipes import Recipe


class RecipeIngredientsAssociation(IdIntPkMixin, Base):
    __tablename__ = "recipe_ingredient_association"

    __table_args__ = (
        UniqueConstraint(
            "recipe_id",
            "ingredient_id",
            name="idx_unique_recipe_ingredient",
        ),
    )

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    amount: Mapped[int] = mapped_column(default=1, server_default="1")

    recipe: Mapped["Recipe"] = relationship(back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship(back_populates="recipe")
