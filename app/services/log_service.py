from typing import NoReturn

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from app.database import DbConnector
from app.models.activity import CurrentActivity, ServicesList, ServicesLog
from app.schemas.base import to_sql
from app.schemas.services_logs_schemas import ServiceLogDB
from app.schemas.services_schemas import ServiceDB
from app.services.service_service import ServicesService


class LogService:
    def __init__(self):
        self.session = DbConnector()
        self.service_service = ServicesService()

    async def get_last_log(self, service_name: str):
        last_log = await self.session.execute(
            select(ServiceLogDB)
            .where(ServiceLogDB.service_name == service_name)
            .order_by(ServiceLogDB.created_date.desc())
            .limit(1)
        )
        return last_log[0]['ServiceLogDB'] if last_log else None

    async def list_logs(self, service_name: str) -> list:
        service_name = service_name.lower()  # ToDO : проверки нужны по шаблонам и тд, тк дыра в безопасности
        result = await self.session.execute(
            select(*to_sql(ServicesLog)).select_from(ServiceLogDB).where(ServiceLogDB.service_name == service_name)
        )
        return [ServicesLog(**_) for _ in result] if result else []

    async def log_activity(self, data: CurrentActivity) -> NoReturn:

        data.service_name = data.service_name.lower()  # ToDO : проверки нужны по шаблонам и тд, тк дыра в безопасности

        service_data = await self.service_service.get_service_data(data)
        last_log = await self.get_last_log(data.service_name)

        current_log_date = await self.session.execute(
            insert(ServiceLogDB).values(**data.__dict__).returning(ServiceLogDB.created_date)
        )
        current_log_created_date = current_log_date[0]['created_date']
        status_map = service_data.status_map
        all_time = status_map.get('time_all', 0)

        delta_time = 0
        if last_log:
            delta_time = (current_log_created_date - last_log.created_date).total_seconds()
            if not status_map.get(last_log.status):
                status_map[last_log.status] = 0
            status_map[last_log.status] += delta_time

        status_map['all_time'] = all_time + delta_time

        await self.session.execute(
            update(ServiceDB).values({'status_map': status_map}).where(ServiceDB.service_name == data.service_name)
        )
