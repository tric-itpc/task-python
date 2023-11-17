from datetime import datetime
from fastapi import APIRouter

from Repositories.ServiceRepo import ServiceRepo
from model.service import Service


router = APIRouter(prefix="/service", tags=['/service'])


@router.get("/")
async def get_all():
    return await ServiceRepo.get_all()


@router.get("/actual_state_service")
async def actual_state_service():
    return await ServiceRepo.get_actual_state_service()


@router.get("/get_state_data")
async def get_state_data(state: str):
    return await ServiceRepo.get_state_data(state)


@router.get("/get_sla")
async def get_state_data(name: str, date_start: datetime, date_end: datetime):
    return await ServiceRepo.get_sla(name, date_start, date_end)


@router.get("/get_service_by_name")
async def get_service_by_name(name: str):
    return await ServiceRepo.get_service_by_name(name)


@router.post("/add_service", status_code=201)
async def add_tabel(service: Service):
    _service = await ServiceRepo.insert(service)
    return _service


@router.delete("/delete", status_code=200)
async def delete_user(id: str):
    await ServiceRepo.delete_one(id)
