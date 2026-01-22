from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IdIntPkMixin
#from core.models.subscription import Subscription

if TYPE_CHECKING:
    from core.models import Subscription

class User(IdIntPkMixin, Base):
    username: Mapped[str] = mapped_column(String(150), unique=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))
    password: Mapped[str] = mapped_column(String(256))
    avatar: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        default=None,
    )

    author: Mapped[List["Subscription"]] = relationship(
        back_populates="subscriber", foreign_keys="Subscription.subscriber_id", lazy="selectin"
    )
    subscriber: Mapped[List["Subscription"]] = relationship(
        back_populates="author", foreign_keys="Subscription.author_id", lazy="selectin"
    )

    @property
    def subscribers_count(self):
        return len(self.subscriber)
    
    @property
    def subscribe_count(self):
        return len(self.author)

    # as_subscriber: Mapped[List["User"]] = relationship(
    #     "User",
    #     back_populates="sbscriber",
    #     secondary=Subscription.__table__,
    # )

    # as_author: Mapped[List["User"]] = relationship(
    #     "User",
    #     back_populates="author",
    #     secondary=Subscription.__table__,
    # )

    # subscriptions_as_subscriber: Mapped[List[Subscriptions]] = relationship(
    #     "Subscriptions",
    #     foreign_keys="Subscriptions.subscriber_id",
    #     back_populates="subscriber",
    #     cascade="all, delete-orphan",
    #     lazy="selectin",  # или "joined" для eager loading,
    #     secondary=Subscriptions.__table__,

    # )
    
    # # Подписки где этот пользователь является автором (на него подписаны)
    # subscriptions_as_author: Mapped[List[Subscriptions]] = relationship(
    #     "Subscriptions",
    #     foreign_keys="Subscriptions.author_id",
    #     back_populates="author",
    #     cascade="all, delete-orphan",
    #     secondary=Subscriptions.__table__,
    # )