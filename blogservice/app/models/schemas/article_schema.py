from pydantic import BaseModel

from .base_schema import BaseSchema


class ArticleBase(BaseModel):
    title: str
    content: str
    category: str


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(ArticleBase):
    title: str | None
    content: str | None
    category: str | None


class ArticleRead(BaseSchema, ArticleBase):
    author_id: int
