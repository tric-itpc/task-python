from typing import Literal

from sqlalchemy.orm import Mapped, mapped_column

from .db_base import Base


class Service(Base):
    service_name: Mapped[str]
    service_description: Mapped[str]
    service_state: Mapped[Literal["stable", "unstable", "disable"]]





