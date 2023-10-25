from pydantic import BaseModel
import uuid
from typing import Literal

import datetime as dt

class ServiceStatusInSchema(BaseModel):
    name: str
    service_status: Literal['online', 'unstable', 'offline',]
    description: str = None
    
class ServiceStatusOutSchema(ServiceStatusInSchema):
    id: uuid.UUID
    created_at: dt.datetime