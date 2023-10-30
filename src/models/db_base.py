import uuid

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import UUID as UUID_SQL, text


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        UUID_SQL,
        nullable=False,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
        unique=True,
        primary_key=True
    )

