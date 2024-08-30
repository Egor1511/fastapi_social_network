from typing import Optional

from ...models.schemas.user_schema import UserCreate, UserRead, UserUpdate
from ...models.user_model import User
from .sqlalchemy_repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository[User, UserCreate, UserUpdate, UserRead]):

    async def get_by_email(self, email: str) -> Optional[UserRead]:
        return await self.find_one_or_none(email=email)


user_repository = UserRepository(User, UserRead)
