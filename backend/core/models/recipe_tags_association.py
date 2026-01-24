from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IdIntPkMixin

if TYPE_CHECKING:
    from .recipes import Recipe
    from .tags import Tag

class RecipeTagsAssociation(IdIntPkMixin, Base):
    __tablename__ = "recipe_tag_association"

    __table_args__ = (
        UniqueConstraint(
            "recipe_id",
            "tag_id",
            name="idx_unique_recipe_tag",
        ),
    )

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))

    recipe: Mapped["Recipe"] = relationship(back_populates="tags")
    tag: Mapped["Tag"] = relationship(back_populates="recipes")