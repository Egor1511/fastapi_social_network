from typing import Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from app.db.database import async_session_maker
from app.db.repositories.base_repository import AbstractRepository
from app.models.article_model import Article
from app.models.comment_model import Comment
from app.models.user_model import User

ModelType = TypeVar("ModelType", bound=Union[Article, User, Comment])
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)


class SqlAlchemyRepository(AbstractRepository, Generic[ModelType, CreateSchemaType, UpdateSchemaType, ReadSchemaType]):

    def __init__(self, model: Type[ModelType], read_schema: Type[ReadSchemaType]):
        self.model = model
        self.read_schema = read_schema

    async def find_one_or_none_by_id(self, data_id: int) -> Optional[ReadSchemaType]:
        async with async_session_maker() as session:
            query = select(self.model).filter_by(id=data_id)
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
            if instance:
                return self.read_schema.from_orm(instance)
            return None

    async def find_one_or_none(self, **filter_by) -> Optional[ReadSchemaType]:
        async with async_session_maker() as session:
            query = select(self.model).filter_by(**filter_by)
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
            if instance:
                return self.read_schema.from_orm(instance)
            return None

    async def get(self, **filter_by) -> List[ReadSchemaType]:
        async with async_session_maker() as session:
            query = select(self.model).filter_by(**filter_by)
            result = await session.execute(query)
            instances = result.scalars().all()
            return [self.read_schema.from_orm(instance) for instance in instances]

    async def create(self, data: CreateSchemaType) -> ReadSchemaType:
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = self.model(**data.dict())
                session.add(new_instance)
                try:
                    await session.flush()
                    await session.refresh(new_instance)
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return self.read_schema.from_orm(new_instance)

    async def add_many(self, instances: List[CreateSchemaType]) -> List[ReadSchemaType]:
        async with async_session_maker() as session:
            async with session.begin():
                new_instances = [self.model(**data.dict()) for data in instances]
                session.add_all(new_instances)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return [self.read_schema.from_orm(instance) for instance in new_instances]

    async def update(self, data: UpdateSchemaType, **filter_by) -> ReadSchemaType:
        async with async_session_maker() as session:
            async with session.begin():
                stmt = (
                    sqlalchemy_update(self.model)
                    .where(*[getattr(self.model, k) == v for k, v in filter_by.items()])
                    .values(**data.dict(exclude_unset=True))
                    .returning(self.model)
                )
                result = await session.execute(stmt)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                updated_instance = result.scalar_one()
                return self.read_schema.from_orm(updated_instance)

    async def delete(self, delete_all: bool = False, **filter_by) -> int:
        if delete_all is False and not filter_by:
            raise ValueError("Необходимо указать хотя бы один параметр для удаления.")

        async with async_session_maker() as session:
            async with session.begin():
                query = sqlalchemy_delete(self.model).filter_by(**filter_by)
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount
