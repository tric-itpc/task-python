from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVER_HOST: str = 'localhost'
    SERVER_PORT: int = 8099
    TITLE_API: str = 'TEST'
    DOC_URL: str = '/docs'
    VERSION: str = 'v1.0'

    SQL_ASYNC_CONNECT: str = 'postgresql+asyncpg://test_user:test_pass@test_postgres:5432/test_db'
    DROP_DATABASE: bool = None


settings = Settings(
    _env_file='../.env',
    _env_file_encoding='utf-8',
)
