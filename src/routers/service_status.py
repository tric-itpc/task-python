from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.schemas.service_status import ServiceStatusInSchema, ServiceStatusOutSchema
from src.services.service_status import post

router = APIRouter(
    prefix='/services_statuses'
)

@router.post('/add/', summary='Добавить новый сервис и статус для него, либо обновить статус существующего сервиса', response_model=ServiceStatusOutSchema)
async def service_status_add(payload: ServiceStatusInSchema, session: AsyncSession = Depends(get_session)):
    try:
        status = await post(payload, session)
        session.add(status)
        await session.commit()  
        return {
            "id": status.id,
            "name": status.name,
            "service_status": status.service_status,
            "description": status.description,
            "created_at": status.created_at
        }
    except ValueError:
        raise HTTPException(status_code=400, detail='Данный статус для указанного сервиса уже является актуальным')
