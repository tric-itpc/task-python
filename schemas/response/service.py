from models.enums import Status
from schemas.base import BaseService


class ServiceOut(BaseService):
    id: int


class ServiceAndStateOut(ServiceOut):
    status: Status
