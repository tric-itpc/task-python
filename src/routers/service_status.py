from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from src.database import get_session
from src.schemas.service_status import ServiceStatusInSchema, ServiceStatusOutSchema
from src.services.service_status import post, get_list, retrieve

router = APIRouter(
    prefix='/services_statuses'
)

@router.post('/add/', summary='Добавить новый сервис и статус для него, либо обновить статус существующего сервиса', response_model=ServiceStatusOutSchema)
async def add(payload: ServiceStatusInSchema, session: AsyncSession = Depends(get_session)):
    try:
        result = await post(payload, session)
        session.add(result)
        await session.commit()  
        return {
            "id": result.id,
            "name": result.name,
            "service_status": result.service_status,
            "description": result.description,
            "created_at": result.created_at
        }
    except ValueError:
        raise HTTPException(status_code=400, detail='Данный статус для указанного сервиса уже является актуальным')
    
@router.get('/list/', summary='Получить список актуальных состояний для каждого сервиса', response_model=List[ServiceStatusOutSchema])
async def list(session: AsyncSession = Depends(get_session)):
    statuses_list = await get_list(session)
    return [
        {
            'name': st.name,
            'service_status': st.service_status,
            'description': st.description,
            'id': st.id,
            'created_at': st.created_at
        }
    for st in statuses_list]

@router.get('/retrieve/', summary='История всех состояний для интересующего сервиса', response_model=List[ServiceStatusOutSchema])
async def get(name: str, session: AsyncSession = Depends(get_session)):
    service_history = await retrieve(name, session)
    return service_history
    
    