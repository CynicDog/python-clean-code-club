from fastapi import Depends, APIRouter

from typing import List
from ..models.post import Post, PostPagination
from ..dependencies import get_post_or_404
from ..internal.database import mock_db

router = APIRouter(prefix="/posts", tags=["post"])
post_pagination = PostPagination(maximum_limit=50)


@router.get("/{id}", response_model=Post)
async def get(post: Post = Depends(get_post_or_404)):
    """
    Get a single post.

    Example:
        http ":8000/posts/1"

    :param post: The post object injected by the dependency
    :return: A single Post model
    """
    return post


@router.get("/", response_model=List[Post])
async def get_posts_paginated(p: tuple[int, int] = Depends(post_pagination)):
    """
    Get a list of posts.

    Example:
        http ":8000/posts/?skip=0&limit=20"

    :param p: A tuple containing (skip, limit)
    :return: A list of Post models
    """
    skip, limit = p
    return list(mock_db.values())[skip : skip+limit]