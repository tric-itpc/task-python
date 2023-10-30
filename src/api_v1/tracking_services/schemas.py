from typing import Literal

from pydantic import BaseModel


class CreateService(BaseModel):
    service_name: str
    service_description: str
    service_state: Literal["stable", "unstable", "disable"]

