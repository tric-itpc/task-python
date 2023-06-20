from sqlalchemy.exc import OperationalError, ResourceClosedError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.schemas.base import Base
from app.settings import settings

engine = create_async_engine(settings.SQL_ASYNC_CONNECT, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class DbConnector:
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
