from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from app.db.repositories.sqlalchemy_repository import ModelType, ReadSchemaType, SqlAlchemyRepository, UpdateSchemaType


class BaseService:
    def __init__(self, repository: SqlAlchemyRepository):
        self.repository = repository

    async def find_by_id(self, data_id: int) -> Optional[ReadSchemaType]:
        return await self.repository.find_one_or_none_by_id(data_id)

    async def find_one(self, **filter_by) -> Optional[ReadSchemaType]:
        return await self.repository.find_one_or_none(**filter_by)

    async def get_all(self, **filter_by) -> List[ReadSchemaType]:
        return await self.repository.get(**filter_by)

    async def create(self, model: UpdateSchemaType) -> ReadSchemaType:
        return await self.repository.create(data=model)

    async def update(self, data: UpdateSchemaType, **filter_by: Any) -> ReadSchemaType:
        return await self.repository.update(data=data, **filter_by)

    async def delete(self, **filter_by: Any) -> int:
        return await self.repository.delete(**filter_by)
