from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.service import SLA_output
from func import service as ServiceCrud

from schemas import service as ServiceSchema

router = APIRouter()

@router.post('/', tags=(["service"]))
async def create(data:ServiceSchema.Service = None, db: Session = Depends(get_db)):
    return ServiceCrud.create_service(data, db)

@router.get('/get_services', tags=(["service"]))
async def get(db: Session = Depends(get_db)):
    return ServiceCrud.get_service(db)

@router.put('/{name}', tags=(["service"]))
async def update(data:ServiceSchema.Service = None, name: str = None, db: Session = Depends(get_db)):
    return ServiceCrud.update_service(data, db, name)

@router.get('/history/{service_name}', tags=(["service"]))
async def get(service_name: str = None, db: Session = Depends(get_db)):
    return ServiceCrud.get_service_history(service_name, db)

@router.get('/{state}', tags=(["service"]))
async def get_services_by_state(state: str = None, db: Session = Depends(get_db)):
    return ServiceCrud.get_services_by_state(state, db)

@router.get('/sla/{name}', tags=(["service"]), response_model=SLA_output)
async def calculate_sla(name: str = None, start: str = None, end: str = None, db: Session = Depends(get_db)):
    return ServiceCrud.calculate_sla(name, db, start, end)

