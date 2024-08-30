from ...models.comment_model import Comment
from ...models.schemas.comment_schema import CommentCreate, CommentRead, CommentUpdate
from .sqlalchemy_repository import SqlAlchemyRepository


class CommentRepository(SqlAlchemyRepository[Comment, CommentCreate, CommentUpdate, CommentRead]):
    pass


comment_repository = CommentRepository(Comment, CommentRead)
