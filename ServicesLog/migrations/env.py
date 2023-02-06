from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

from settings import config as app_config
from utils.database.accessor import PostgresAccessor
from utils.database.models import gino as db

config = context.config
fileConfig(config.config_file_name)
target_metadata = db


def run_migrations_online():
    PostgresAccessor()
    connectable = create_engine(app_config["postgres"]["database_url"])
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()