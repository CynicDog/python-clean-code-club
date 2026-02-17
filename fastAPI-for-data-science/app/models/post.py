from pydantic import BaseModel
from fastapi import Query


class PostBase(BaseModel):
    title: str
    content: str

class Post(PostBase):
    id: int
    views: int = 0

class PostPagination:
    def __init__(self, maximum_limit: int = 100):
        self.maximum_limit = maximum_limit

    async def __call__(
            self,
            skip: int = Query(0, ge=0),
            limit: int = Query(10, ge=0),
    ) -> tuple[int, int]:
        return skip, min(self.maximum_limit, limit)