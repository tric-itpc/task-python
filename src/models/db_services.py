from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from .db_base import Base

if TYPE_CHECKING:
    from .db_service_state import ServiceState


class Service(Base):
    service_name: Mapped[str] = mapped_column(unique=True)
    service_description: Mapped[str]
    state: Mapped["ServiceState"] = relationship(
        back_populates="service",
        order_by="desc(ServiceState.created_at)"
    )
    all_states: Mapped[list["ServiceState"]] = relationship(
        order_by="desc(ServiceState.created_at)"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.service_name!r})"

    def __repr__(self):
        return str(self)





