import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import select

from ..models.base import Base
from ..models.post import Post


DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_db"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)
async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

# A per-request resource manager implemented as a coroutine.
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def create_all_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_posts() -> None:
    async with async_session_maker() as session:
        result = await session.execute(select(Post))
        existing = result.scalars().first()

        if existing:
            return

        posts = [
            Post(title=f"Post {i}", content=f"Content {i}") for i in range(1, 6)
        ]

        session.add_all(posts)
        await session.commit()