from .sqlalchemy_repository import SqlAlchemyRepository
from ...models.comment_model import Comment
from ...models.schemas.comment_schema import CommentCreate, CommentUpdate


class CommentRepository(SqlAlchemyRepository[Comment, CommentCreate, CommentUpdate]):
    def __init__(self, session):
        super().__init__(Comment, session)
