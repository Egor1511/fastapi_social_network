from pydantic import BaseModel

from .base_schema import BaseSchema


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    article_id: int
    author_id: int


class CommentUpdate(CommentBase):
    content: str | None


class CommentRead(BaseSchema, CommentBase):
    article_id: int
    author_id: int
