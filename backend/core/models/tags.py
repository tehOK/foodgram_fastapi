from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IdIntPkMixin

if TYPE_CHECKING:
    from .recipe_tags_association import RecipeTagsAssociation


class Tag(IdIntPkMixin, Base):
    name: Mapped[str] = mapped_column(String(32))
    slug: Mapped[str] = mapped_column(unique=True)

    recipes: Mapped[list["RecipeTagsAssociation"]] = relationship(
        back_populates="tag",
    )