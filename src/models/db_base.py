import uuid

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import UUID as UUID_SQL, text


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[str] = mapped_column(
        UUID_SQL,
        nullable=False,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
        unique=True,
        primary_key=True
    )

