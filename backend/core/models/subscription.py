from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins import IdIntPkMixin

if TYPE_CHECKING:
    from core.models import User


class Subscription(IdIntPkMixin, Base):
    subscriber_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    __table_args__ = (
        UniqueConstraint("subscriber_id", "author_id", name="unique_subscription"),
    )
    subscriber: Mapped["User"] = relationship(
        back_populates="author", foreign_keys=[subscriber_id]
    )
    author: Mapped["User"] = relationship(
        back_populates="subscriber", foreign_keys=[author_id]
    )

    # subscriber = relationship("User", foreign_keys=[subscriber_id], back_populates="subscriptions_as_subscriber")
    # author = relationship("User", foreign_keys=[author_id], back_populates="subscriptions_as_author")
    