from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    publication_date: datetime = Field(default_factory=datetime.now)
    content: str


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: int
    post_id: int
