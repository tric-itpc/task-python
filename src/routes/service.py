from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status

from classes.dependencies import get_services, get_statistic_service
from classes.enums import Status
from classes.interfaces import IRepository, IStatisticService
from classes.validation import (
    service_create,
    service_model,
    service_statistic,
    service_status,
    sla_object,
)
from settings import env

service_router = APIRouter(prefix="/service", tags=["service"])


@service_router.get("/", response_model=List[service_model])
async def get_services_state_list(db: IRepository = Depends(get_services)):
    return db.get()


@service_router.get("/{name}", response_model=service_status)
async def get_service_statistics(
    name: str,
    start: datetime = None,
    end: datetime = None,
    db: IRepository = Depends(get_services),
    statistic_service: IStatisticService = Depends(get_statistic_service),
):
    if start is None:
        start = datetime.now() - timedelta(hours=12)
    if end is None:
        end = datetime.now()
    if start >= end:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail=env.MSG_TIME_INTERVAL_ERROR
        )
    try:
        # получаем все сервисы по имени
        services = db.get(service=name)
        if len(services) == 0:
            raise
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=env.MSG_NOT_FOUND_ERROR)

    # конфигурируем сервис статистики
    statistic_service.set_collection(services)
    statistic_service.set_interval(start, end)

    disabled_time = unstable_time = enabled_time = 0.0

    # если сервис не работал хоть раз, то считаем это время
    if any(i.status == Status.DISABLED.value for i in services):
        disabled_time = statistic_service.summary_time_by_status(Status.DISABLED)

    # если сервис работал хоть раз, то считаем это время
    if any(i.status == Status.ENABLED.value for i in services):
        enabled_time = statistic_service.summary_time_by_status(Status.ENABLED)

    # если сервис был нестабилен хоть раз, то считаем это время
    if any(i.status == Status.UNSTABLE.value for i in services):
        unstable_time = statistic_service.summary_time_by_status(Status.UNSTABLE)

    # считаем SLA
    uptime, availability = statistic_service.sla_calculate(
        enabled_time + unstable_time + disabled_time, disabled_time, unstable_time
    )

    # создаем response
    result = service_status(
        service=name,
        interval=(start, end),
        statistic=service_statistic(
            enable_time=enabled_time,
            disabled_time=disabled_time,
            unstable_time=unstable_time,
            SLA=sla_object(uptime=uptime, availability=availability),
        ),
    )
    return result


@service_router.get("/log/{name}", response_model=List[service_model])
async def get_service_log(name: str, db: IRepository = Depends(get_services)):
    try:
        services = db.get(service=name)
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=env.MSG_NOT_FOUND_ERROR)
    return services


@service_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=service_model
)
async def create_service_state(
    content: service_create = Body(), db: IRepository = Depends(get_services)
):
    service = {}

    try:
        service = service_model.create_as_dict(**content.model_dump())
    except:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=env.MSG_ASSOCIATION_ERROR,
        )

    try:
        Status(service[env.PARAM_STATUS])
    except:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=env.MSG_INVALID_STATUS)

    try:
        service.update({env.PARAM_ID: db.add(element=service)})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=env.MSG_CREATING_ERROR,
        )

    return service


@service_router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_state(name: str, db: IRepository = Depends(get_services)):
    try:
        db.remove(service=name)
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=env.MSG_NOT_FOUND)