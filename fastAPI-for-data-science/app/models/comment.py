from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"),
        nullable=False
    )
    publication_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False,
        default=datetime.now
    )
    content: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    post: Mapped["Post"] = relationship("Post", back_populates="comments")