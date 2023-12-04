from datetime import datetime

from sqlalchemy import BIGINT, TIMESTAMP, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.schema import Column


class Base(DeclarativeBase):
    type_annotation_map = {
        int: BIGINT,
        datetime: TIMESTAMP(timezone=False),
        str: String(),
    }

    created_date: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)
    update_date: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


def to_sql(pidantic_schemas):
    """Convert Pydantic schemas to column names"""
    keys = pidantic_schemas.__fields__.keys()
    keys = [Column(key) for key in keys]
    return keys
