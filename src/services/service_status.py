from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text

import datetime as dt

from src.models.service_status import ServiceStatus
from src.schemas.service_status import ServiceStatusInSchema

async def post(payload: ServiceStatusInSchema, session: AsyncSession):
    new_status = ServiceStatus(name=payload.name, service_status=payload.service_status, description=payload.description, created_at=dt.datetime.now())   
    if await latest_status_simmilar(name=payload.name, service_status=payload.service_status, session=session) is True:
        raise ValueError
    return new_status

# Функция для проверки наличия в базе данных записей с таким же полем name.
# Если есть такие записи и при этом последняя среди них обладает таким же значением поля service_status, то новая запись не добавляется в бд
async def latest_status_simmilar(name: str, service_status: str, session: AsyncSession):
    latest_status = await session.execute(select(ServiceStatus).filter_by(name=name).order_by(ServiceStatus.created_at.desc()))
    try:
        if latest_status.scalar().service_status == service_status:
            return True
    except AttributeError:
        return False
                                
async def get_list(session: AsyncSession):
    stmt = text(
        '''SELECT st1.*
FROM statuses as st1
JOIN (SELECT st2.name, MAX(st2.created_at) AS latest_time
	 FROM statuses AS st2
	 GROUP BY st2.name) as st2
ON st1.name = st2.name
WHERE st1.created_at = st2.latest_time'''
    )
    # stmt = select(ServiceStatus).group_by(ServiceStatus.name)  
    result = await session.execute(stmt)
    return result