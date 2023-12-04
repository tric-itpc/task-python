from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # SQLALCHEMY_URL: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres 2'
    DROP_DATABASE: bool = False

    DB_HOST: str = 'localhost'
    DB_PORT: str = '5432'
    DB_NAME: str = 'postgres 2'
    DB_USER: str = 'postgres'
    DB_PASS: str = 'postgres'

settings = Settings(
    _env_file='../.env',
    _env_file_encoding='utf-8',
)
