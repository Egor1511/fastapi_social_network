from app.db.repositories.article_repository import ArticleRepository, article_repository
from app.models.article_model import Article
from app.models.schemas.article_schema import ArticleRead
from app.services.base_service import BaseService


class ArticleService(BaseService):
    async def find_by_id(self, article_id: int) -> ArticleRead | None:
        article = await self.repository.find_one_or_none_by_id(article_id)
        if not article:
            return None
        return article


article_service = ArticleService(repository=article_repository)
