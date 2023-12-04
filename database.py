from sqlalchemy.exc import OperationalError, ResourceClosedError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from schemas.base import Base
from settings import settings
import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_URL = settings.SQLALCHEMY_URL

SQLALCHEMY_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres10"
engine = create_async_engine(SQLALCHEMY_URL, echo=False, pool_pre_ping=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)



class get_db:
    def __init__(self):
        pass

    async def create_tables(self) -> None:
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except OperationalError as error:
            pass

    async def drop_tables(self) -> None:
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
        except OperationalError as error:
            pass

    async def insert(self, stmt: Base) -> None:
        try:
            async with async_session() as session:
                async with session.begin():
                    session.add(stmt)
                    await session.commit()
        except OperationalError as error:
            pass

    async def execute(self, stmt: Base) -> list | None:
        try:
            async with async_session() as session:
                async with session.begin():
                    result = await session.execute(stmt)
                    try:
                        result = [u._asdict() for u in result.all()]
                    except ResourceClosedError:
                        return None
                    return result if len(result) > 0 else None

        except OperationalError as error:
            pass
