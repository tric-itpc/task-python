from typing import List
from fastapi import APIRouter, Depends

from models.activity import CurrentActivity, ServicesList, ServicesLog
from services.log_service import LogService
from services.service_service import ServicesService

router = APIRouter(prefix='/logs', tags=['Logs'])

"""Фиксируем активность сервера"""
@router.post('/save_logs/')
async def log_activity(
    data: CurrentActivity,
    activity_service: LogService = Depends(),
):

    return await activity_service.log_activity(data)

"""Список всех серверов"""
@router.get('/list_services/', response_model=List[ServicesList] | None)
async def list_services(
    service_service: ServicesService = Depends(),
):

    return await service_service.list_services()

"""Логи сервера"""
@router.get('/list_logs/', response_model=List[ServicesLog])
async def list_logs(
    service_name: str,
    activity_service: LogService = Depends(),
):
    return await activity_service.list_logs(service_name)
