from db import database
from models import service


class ServiceManager:
    @staticmethod
    async def get_services():
        query = service.select()
        return await database.fetch_all(query)

    @staticmethod
    async def create_service(service_data):
        id_ = await database.execute(service.insert().values(service_data))
        return await database.fetch_one(
            service.select().where(service.c.id == id_)
        )

    @staticmethod
    async def update_service(service_id, service_data):
        await database.execute(
            service.update()
            .where(service.c.id == service_id)
            .values(service_data)
        )

    @staticmethod
    async def delete_service(service_id):
        await database.execute(
            service.delete().where(service.c.id == service_id)
        )
