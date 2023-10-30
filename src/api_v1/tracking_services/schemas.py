from datetime import datetime
import uuid
from typing import Literal

from pydantic import BaseModel


class CreateServiceSchema(BaseModel):
    service_name: str
    service_description: str
    state: Literal["stable", "unstable", "disable"]


class ServiceStateSchema(BaseModel):
    service_id: uuid.UUID
    service_state: Literal["stable", "unstable", "disable"]


