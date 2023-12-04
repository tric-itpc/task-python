from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select

from database import get_db
from models.activity import CurrentActivity, ServicesList
from schemas.base import to_sql
from schemas.services_schemas import ServiceDB


class ServicesService:
    def __init__(self):
        self.session = get_db()

    async def get_service_data(self, data: CurrentActivity) -> ServiceDB:
        service_data = await self.session.execute(select(ServiceDB).where(ServiceDB.service_name == data.service_name))
        if service_data:
            return service_data[0]['ServiceDB']

        service_data = await self.session.execute(insert(ServiceDB).values(**data.__dict__).returning(ServiceDB))
        return service_data[0]['ServiceDB']

    async def list_services(self):
        result = await self.session.execute(select(*to_sql(ServicesList)).select_from(ServiceDB))
        return result
