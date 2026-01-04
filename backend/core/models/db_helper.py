from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession

from config import settings

class DBHelper:
    def __init__(
            self,
            url: str,
            echo: bool = False,
        ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session

db_helper = DBHelper(
    url=settings.db.db_url,
    echo=settings.db.echo,
)