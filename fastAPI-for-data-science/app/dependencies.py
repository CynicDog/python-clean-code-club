from fastapi import Header, HTTPException, status
from typing import Annotated

from .models.post import Post
from .internal.database import mock_db


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")


async def get_post_or_404(id: int) -> Post:
    post = mock_db.get(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {id} not found"
        )
    return post
