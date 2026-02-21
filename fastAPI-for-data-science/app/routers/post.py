from typing import List
from collections.abc import Sequence

from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..internal.database import get_async_session
from ..dto.post import PostRead, PostCreate, PostUpdate, PostPagination
from ..dto.comment import CommentRead, CommentCreate
from ..models.post import Post
from ..models.comment import Comment
from ..repository.post import (
    get_post_by_id,
    list_posts_all,
    list_posts_paginated,
    create_post,
    update_post,
    delete_post,
    create_comment,
)

router = APIRouter(prefix="/posts", tags=["post"])
post_pagination = PostPagination(maximum_limit=50)


@router.get("/all", response_model=List[PostRead])
async def read_all_posts_route(
    session: AsyncSession = Depends(get_async_session),
) -> Sequence[Post]:
    """
    Get all posts.

    Example:
        http ":8000/posts/all"

    :param session: The session object injected by the dependency
    :return: A list of Post model
    """
    return await list_posts_all(session)


@router.get("/", response_model=List[PostRead])
async def read_posts_paginated_route(
    pagination: tuple[int, int] = Depends(post_pagination),
    session: AsyncSession = Depends(get_async_session),
) -> Sequence[Post]:
    """
    Get all posts paginated.

    Example:
        http ":8000/posts/?limit=10&offset=0"

    :param pagination: A tuple containing skip and limit values
    :param session: The session object injected by the dependency

    :return: A paginated list of Post model
    """
    skip, limit = pagination
    return await list_posts_paginated(session, skip, limit)


@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post_route(
    post_create: PostCreate,
    session: AsyncSession = Depends(get_async_session),
) -> Post:
    """
    Create a new post.

    Example:
        echo '{"title": "Hello FastAPI", "content": "My first post"}' \
        | http POST :8000/posts/ --json

    :param post_create: The post object received in request body
    :param session: The session object injected by the dependency

    :return: A newly created Post model
    """
    return await create_post(session, post_create)


@router.get("/{id}", response_model=PostRead)
async def read__post_route(
    id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Post:
    """
    Get a single post.

    Example:
        http ":8000/posts/1"

    :param id: The post id passed by request
    :param session: The session object injected by the dependency

    :return: A single Post model
    """
    post = await get_post_by_id(session, id)

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.put("/{id}", response_model=PostRead)
async def update_post_route(
    id: int,
    post_update: PostUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> Post:
    """
    Update a post.

    Example:
        http PUT :8000/posts/1 title="Updated" content="New content"

    :param id: The post id passed by request
    :param post_update: Updated post data
    :param session: The session object injected by dependency

    :return: Updated Post model
    """
    post = await update_post(session, id, post_update)

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_route(
    id: int,
    session: AsyncSession = Depends(get_async_session),
) -> None:
    """
    Delete a post.

    Example:
        http DELETE :8000/posts/1

    :param id: The post id passed by request
    :param session: The session object injected by dependency
    """
    deleted = await delete_post(session, id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")

    return None


@router.post(
    "/{id}/comments", response_model=CommentRead, status_code=status.HTTP_201_CREATED
)
async def create_post_comment_route(
    id: int,
    comment_create: CommentCreate,
    session: AsyncSession = Depends(get_async_session),
) -> Comment:
    """
    Create a new comment.

    Example:
        echo '{"content": "This is a comment"}' \
        | http POST :8000/posts/1/comments --json

    :param comment_create: The comment object received in request body
    :param session: The session object injected by the dependency
    """
    return await create_comment(session, comment_create, post_id=id)
