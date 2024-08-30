from sqlalchemy import select

from ...models.article_model import Article
from ...models.comment_model import Comment
from ...models.schemas.article_schema import ArticleCreate, ArticleRead, ArticleUpdate
from ...models.schemas.comment_schema import CommentRead
from ..database import async_session_maker
from .sqlalchemy_repository import SqlAlchemyRepository


class ArticleRepository(SqlAlchemyRepository[Article, ArticleCreate, ArticleUpdate, ArticleRead]):
    async def get_related_comments(self, article_id: int) -> list[CommentRead]:
        async with async_session_maker() as session:
            query = select(Comment).filter_by(article_id=article_id)
            result = await session.execute(query)
            comments = result.scalars().all()
            return [CommentRead.from_orm(comment) for comment in comments]


article_repository = ArticleRepository(Article, ArticleRead)
