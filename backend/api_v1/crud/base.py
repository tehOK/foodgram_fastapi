from typing import Sequence, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)

class BaseCRUD:
    model = None

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by) -> Sequence[ModelType]:
        query = select(cls.model).filter_by(**filter_by)
        return list(await session.scalars(query))
    
    @classmethod
    async def create(cls, session: AsyncSession, data: CreateSchemaType) -> ModelType:
        create_model = cls.model(**data.model_dump())
        session.add(create_model)
        await session.commit()
        await session.refresh(create_model)
        return create_model
    

    @classmethod
    async def find_by_id(cls, session: AsyncSession, model_id: int) -> ModelType:
        query = select(cls.model).filter_by(id=model_id)
        result = await session.scalars(query)
        return result.one_or_none()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.scalars(query)
        return result.one_or_none()

