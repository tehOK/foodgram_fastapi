from typing import TYPE_CHECKING

from sqlalchemy import select

from api_v1.crud import BaseCRUD
from backend.core.authentication.utils import hash_password, verify_password
from core.exeptions import PasswordExc
from core.models import Subscription, User
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from core.schemas import UserCreate, UserPasswordUpdate, UserRead


class UsersCRUD(BaseCRUD):
    model = User

    @classmethod
    async def get_all_users(cls, session: "AsyncSession") -> Page["UserRead"]:
        query = select(cls.model)
        result = await paginate(session, query=query)
        return result
        

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

    @classmethod
    async def get_user_subscribers(cls, session: "AsyncSession", user: User):
        query = select(User).join(Subscription, Subscription.author_id == User.id).where(Subscription.subscriber_id == user.id)
        result = await session.scalars(query)
        return list(result)
    
    @classmethod
    async def create_subscibe_on_user(cls, session: "AsyncSession", user_id: int, user: User):
        print(user_id)
        print(user)
        subscription = Subscription(
            subscriber_id = user.id,
            author_id = user_id,
        )
        session.add(subscription)
        await session.commit()
        await session.refresh(subscription)

        author = await cls.find_by_id(session=session, model_id=user_id)

        return author
    
    @classmethod
    async def delete_subscribe_on_author(cls, session: "AsyncSession", user_id: int, user: User):
        query = select(Subscription).where(
            (Subscription.subscriber_id == user.id) &
            (Subscription.author_id == user_id)
        )
        result = await session.execute(query)
        subscription = result.scalar_one_or_none()
        print(subscription)
        await session.delete(subscription)
        await session.commit()
        return True