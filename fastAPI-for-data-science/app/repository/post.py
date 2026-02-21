from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..dto.post import PostCreate, PostUpdate
from ..dto.comment import CommentCreate
from ..models.post import Post
from ..models.comment import Comment


async def get_post_by_id(
        session: AsyncSession,
        id: int
) -> Post | None:
    result = await session.execute(
        select(Post)
        .where(Post.id == id)
        .options(selectinload(Post.comments))
    )
    return result.scalar_one_or_none()


async def list_posts_all(session: AsyncSession) -> list[Post]:
    result = await session.execute(
        select(Post)
        .order_by(Post.id)
        .options(selectinload(Post.comments))
    )
    return result.scalars().all()


async def list_posts_paginated(
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


async def create_post(
    session: AsyncSession,
    post_create: PostCreate,
) -> Post:
    post = Post(**post_create.model_dump())

    session.add(post)
    await session.commit()
    await session.refresh(post, attribute_names=["comments"])

    return post


async def update_post(
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
    await session.refresh(post, attribute_names=["comments"])

    return post


async def delete_post(
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


async def create_comment(
    session: AsyncSession,
    comment_create: CommentCreate,
    post_id: int
) -> Comment:
    comment = Comment(**comment_create.model_dump(), post_id=post_id)

    session.add(comment)
    await session.commit()
    await session.refresh(comment)

    return comment