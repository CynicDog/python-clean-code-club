from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..dto.post import PostCreate, PostUpdate
from ..models.post import Post


async def get_by_id(
        session: AsyncSession,
        id: int
) -> Post | None:
    result = await session.execute(
        select(Post)
        .where(Post.id == id)
        .options(selectinload(Post.comments))
    )
    return result.scalar_one_or_none()


async def list_all(session: AsyncSession) -> list[Post]:
    result = await session.execute(
        select(Post)
        .order_by(Post.id)
        .options(selectinload(Post.comments))
    )
    return result.scalars().all()


async def list_paginated(
    session: AsyncSession,
    skip: int,
    limit: int,
) -> list[Post]:
    result = await session.execute(
        select(Post)
        .order_by(Post.id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def create(
    session: AsyncSession,
    post_create: PostCreate,
) -> Post:
    post = Post(**post_create.model_dump())

    session.add(post)
    await session.commit()
    await session.refresh(post)

    return post


async def update(
    session: AsyncSession,
    post_id: int,
    post_update: PostUpdate,
) -> Post | None:
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if post is None:
        return None

    for field, value in post_update.model_dump().items():
        setattr(post, field, value)

    await session.commit()
    await session.refresh(post)

    return post


async def delete(
    session: AsyncSession,
    post_id: int,
) -> bool:
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if post is None:
        return False

    await session.delete(post)
    await session.commit()

    return True