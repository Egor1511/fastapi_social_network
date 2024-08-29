from .sqlalchemy_repository import SqlAlchemyRepository
from ...models.comment_model import Comment
from ...models.schemas.comment_schema import CommentCreate, CommentUpdate
from ...models.schemas.user_schema import UserCreate, UserUpdate
from ...models.user_model import User


class UserRepository(SqlAlchemyRepository[User, UserCreate, UserUpdate]):
    def __init__(self, session):
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> User | None:
        return await self.get_single(email=email)
