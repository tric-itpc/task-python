from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from schemas.base import Base


class ServiceDB(Base):
    __tablename__ = 'services'
    service_name: Mapped[str] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    status_map = mapped_column(JSONB, default={})
