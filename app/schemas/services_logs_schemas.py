from uuid import uuid4

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from app.schemas.base import Base


class ServiceLogDB(Base):
    __tablename__ = 'services_logs'
    log_uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    service_name = mapped_column(ForeignKey('services.service_name'), nullable=True)
    status: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False, default='')
