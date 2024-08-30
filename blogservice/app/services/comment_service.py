from app.db.repositories.comment_repository import CommentRepository, comment_repository
from app.models.comment_model import Comment
from app.services.base_service import BaseService


class CommentService(BaseService):
    pass


comment_service = CommentService(repository=comment_repository)
