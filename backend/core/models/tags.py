from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING

from .base import Base

# if TYPE_CHECKING:
#     from .recipe_tags_association import RecipeTagsAssociation


class Tag(Base):
    name: Mapped[str] = mapped_column(String(32))
    slug: Mapped[str] = mapped_column(unique=True)

    # recipes: Mapped[list["RecipeTagsAssociation"]] = relationship(
    #     back_populates="tag",
    # )