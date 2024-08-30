from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config.database.db_config import settings_db
from app.core.config.database.db_helper import db_helper

DATABASE_URL = settings_db.get_db_url


engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_db_session() -> AsyncSession:
    async with db_helper.get_db_session() as session:
        yield session
