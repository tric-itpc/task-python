import uuid
from datetime import datetime
from typing import Literal, TYPE_CHECKING

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from .db_services import Service


class ServiceState(Base):
    service_state: Mapped[Literal["stable", "unstable", "disable"]]
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
        server_default=text("now()")
    )
    service_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("services.id"))
    service: Mapped["Service"] = relationship(back_populates="state")

    def __str__(self):
        return f"{self.__class__.__name__}: current_state - {self.service_state}, {self.created_at}"

    def __repr__(self):
        return str(self)