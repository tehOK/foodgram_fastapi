from typing import TYPE_CHECKING

from api_v1.crud import BaseCRUD
from auth.utils import hash_password, verify_password
from core.exeptions import PasswordExc
from core.models import User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from core.schemas import UserCreate, UserPasswordUpdate


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
    
    @classmethod
    async def change_password(cls, session: "AsyncSession", password_data: "UserPasswordUpdate", user: "UserCreate"):
        if not verify_password(password=password_data.current_password, hashed_password=user.password):
            raise PasswordExc
        new_hashed_password = hash_password(password=password_data.new_password)
        user.password = new_hashed_password

        session.add(user)

        await session.commit()
        await session.refresh(user)