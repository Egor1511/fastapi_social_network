from typing import Optional

from app.db.repositories.user_repository import UserRepository, user_repository
from app.models.schemas.user_schema import UserRead
from app.models.user_model import User
from app.services.base_service import BaseService


class UserService(BaseService):
    async def get_by_email(self, email: str) -> Optional[UserRead]:
        return await self.repository.find_one_or_none(email=email)


user_service = UserService(repository=user_repository)
