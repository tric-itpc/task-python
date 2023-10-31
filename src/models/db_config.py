import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session

from src.config import DB_USER, DB_PASS, DB_HOST, DB_NAME, DB_PORT

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

current_task = asyncio.current_task


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )

        return session

    def get_scoped_session_dependency(self):
        print("session open")
        session = self.get_scoped_session()
        yield session
        session.close()
        print("session closed")


db_helper = DatabaseHelper(url=DATABASE_URL)

