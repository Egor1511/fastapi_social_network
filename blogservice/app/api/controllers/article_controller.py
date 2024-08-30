from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user
from app.models.schemas.article_schema import ArticleCreate, ArticleRead, ArticleUpdate
from app.models.user_model import User
from app.services.article_service import article_service

router = APIRouter()


@router.post("/", response_model=ArticleRead)
async def create_article(article: ArticleCreate, current_user: User = Depends(get_current_user)):
    article.author_id = current_user.id
    return await article_service.create(article)


@router.get("/{article_id}", response_model=ArticleRead)
async def get_article(article_id: int):
    article = await article_service.find_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.put("/{article_id}", response_model=ArticleRead)
async def update_article(article_id: int, article: ArticleUpdate, current_user: User = Depends(get_current_user)):
    existing_article = await article_service.find_by_id(article_id)
    if not existing_article:
        raise HTTPException(status_code=404, detail="Article not found")
    if existing_article.author_id != current_user.id or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return await article_service.update(article, id=article_id)


@router.delete("/{article_id}")
async def delete_article(article_id: int, current_user: User = Depends(get_current_user)):
    existing_article = await article_service.find_by_id(article_id)
    if not existing_article:
        raise HTTPException(status_code=404, detail="Article not found")
    if existing_article.author_id != current_user.id or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    await article_service.delete(id=article_id)
    return {"detail": "Article deleted"}
