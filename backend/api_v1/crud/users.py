from typing import TYPE_CHECKING

from api_v1.crud import BaseCRUD
from auth.utils import hash_password
from core.models import User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from core.schemas import UserCreate


class UsersCRUD(BaseCRUD):
    model = User

    @classmethod
    async def create_user(cls, session: "AsyncSession", user: "UserCreate") -> User:
        if await cls.find_one_or_none(session=session, username=user.username):
            raise ValueError("User with this username already exists")
        if await cls.find_one_or_none(session=session, email=user.email):
            raise ValueError("User with this email already exists")
        user_data = user.model_dump()
        user_data["password"] = hash_password(user_data["password"])
        db_user = cls.model(**user_data)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user
