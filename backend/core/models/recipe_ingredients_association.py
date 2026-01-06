
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    UniqueConstraint,
    DateTime,
    func,
    Text,
)
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .recipes import Recipe
    from .ingredients import Ingredient

class RecipeIngredientsAssociation(Base):
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