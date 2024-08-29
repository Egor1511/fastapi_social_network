from .sqlalchemy_repository import SqlAlchemyRepository
from ...models.article_model import Article
from ...models.schemas.article_schema import ArticleCreate, ArticleUpdate


class ArticleRepository(SqlAlchemyRepository[Article, ArticleCreate, ArticleUpdate]):
    def __init__(self, session):
        super().__init__(Article, session)
