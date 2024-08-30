from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user
from app.models.schemas.comment_schema import CommentCreate, CommentRead, CommentUpdate
from app.models.user_model import User
from app.services.comment_service import comment_service

router = APIRouter()


@router.post("/", response_model=CommentRead)
async def create_comment(comment: CommentCreate, current_user: User = Depends(get_current_user)):
    return await comment_service.create(comment, author_id=current_user.id)


@router.get("/{comment_id}", response_model=CommentRead)
async def get_comment(comment_id: int):
    comment = await comment_service.find_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.put("/{comment_id}", response_model=CommentRead)
async def update_comment(comment_id: int, comment: CommentUpdate, current_user: User = Depends(get_current_user)):
    existing_comment = await comment_service.find_by_id(comment_id)
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if existing_comment.author_id != current_user.id or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return await comment_service.update(comment, id=comment_id)


@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, current_user: User = Depends(get_current_user)):
    existing_comment = await comment_service.find_by_id(comment_id)
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if existing_comment.author_id != current_user.id or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    await comment_service.delete(id=comment_id)
    return {"detail": "Comment deleted"}
