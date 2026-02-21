from datetime import datetime
from pydantic import BaseModel, Field
from fastapi import Query


class PostBase(BaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    views: int = 0


class PostUpdate(PostBase):
    title: str | None = None
    content: str | None = None


class PostPagination:
    def __init__(self, maximum_limit: int = 100):
        self.maximum_limit = maximum_limit

    async def __call__(
            self,
            skip: int = Query(0, ge=0),
            limit: int = Query(10, ge=0),
    ) -> tuple[int, int]:
        return skip, min(self.maximum_limit, limit)