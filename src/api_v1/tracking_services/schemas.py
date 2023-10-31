import uuid
from typing import Literal
from datetime import datetime

from pydantic import BaseModel


class ServiceState(BaseModel):
    """
    Схема для доступных состояний.
    """
    service_state: Literal["stable", "unstable", "disable"]


class CurrentServiceState(ServiceState):
    """
    Схема для описания имя сервиса и текущего состояния
    """
    service_name: str


class CreateServiceSchema(CurrentServiceState):
    """
    Схема для доавления нового сервиса и его начального
    состояния.
    """
    service_description: str


class ResponseService(BaseModel):
    """
    Схема для ответа на создание нового
    сервиса(если операция успешна, то
    возращается id нового сервиса)
    """
    id: uuid.UUID


class SuccessStartUpdateSchema(BaseModel):
    """
    Схема для ответа, при успешном старте
    модуля для обновлений состояний сервисов.
    """
    status: str = "service_update_started_success"


class SuccessAddServiceToTrack(BaseModel):
    """
    Схема для ответа, при успешном добавлении
    сервиса в модуль для обновлений состояний
    сервисов
    """
    status: str = "Service add to tracking!"


class ServiceFullInformation(BaseModel):
    """
    Схема для для описания полной информации
    о сервисе(кроме id)
    """
    service_name: str
    service_description: str


class ServiceStateHistory(ServiceState):
    """
    Схема для описания состояния и времени
    добавлении записи этого состояния.
    """
    created_at: datetime


class ResponseHistory(BaseModel):
    """
    Схема для описания сервиса и истории
    всех его состояний.
    """
    service_info: ServiceFullInformation
    service_state_history: list[ServiceStateHistory] = []


class AllServiceStates(BaseModel):
    """
    Схема для описания ТЕКУЩЕГО состояния
    всех сервисов присутствующих в БД.
    """
    current_state: list[CurrentServiceState] = []

