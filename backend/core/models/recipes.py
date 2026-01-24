from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IdIntPkMixin
from .recipe_ingredients_association import RecipeIngredientsAssociation
from .recipe_tags_association import RecipeTagsAssociation

if TYPE_CHECKING:
    from .recipe_ingredients_association import RecipeIngredientsAssociation
    from .recipe_tags_association import RecipeTagsAssociation

class Recipe(IdIntPkMixin, Base):

    author: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(256))
    text: Mapped[str] = mapped_column()
    cooking_time: Mapped[int] = mapped_column()
    pub_date: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        default=func.now(),
    )

    tags: Mapped[list["RecipeTagsAssociation"]] = relationship(
        back_populates="recipe",
    )
    ingredients: Mapped[list["RecipeIngredientsAssociation"]] = relationship(
        back_populates="recipe",
    )
