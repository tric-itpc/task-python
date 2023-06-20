from typing import List

from fastapi import APIRouter, Depends

from app.models.activity import CurrentActivity, ServicesList, ServicesLog
from app.services.log_service import LogService
from app.services.service_service import ServicesService

router = APIRouter(prefix='/grafana', tags=['Grafana'])


@router.post('/log_activity/')
async def log_activity(
    data: CurrentActivity,
    activity_service: LogService = Depends(),
):
    """Логируем активность сервисов"""
    return await activity_service.log_activity(data)


@router.get('/list_services/', response_model=List[ServicesList] | None)
async def list_services(
    service_service: ServicesService = Depends(),
):
    """Список всех"""
    return await service_service.list_services()


@router.get('/list_logs/', response_model=List[ServicesLog])
async def list_logs(
    service_name: str,
    activity_service: LogService = Depends(),
):
    """Логи"""
    return await activity_service.list_logs(service_name)
