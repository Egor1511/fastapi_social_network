from typing import List

from pydantic import BaseModel

from .base_schema import BaseSchema
from .comment_schema import CommentRead


class ArticleBase(BaseModel):
    title: str
    content: str
    category: str | None


class ArticleCreate(ArticleBase):
    author_id: int | None


class ArticleUpdate(ArticleBase):
    title: str | None = None
    content: str | None = None
    category: str | None = None


class ArticleRead(BaseSchema):
    title: str
    category: str
    author_id: int


class ArticleDetailRead(BaseSchema, ArticleBase):
    author_id: int
    comments: list[CommentRead] = []

    class Config:
        from_attributes = True
