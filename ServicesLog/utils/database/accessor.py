from aiohttp import web

class PostgresAccessor:
    def __init__(self) -> None:
        self.db = None
        
        from utils.database.models import gino
        self.gino = gino

        from app.models import ServicesList, ServicesStatusesList
        self.services_list = ServicesList
        self.services_statuses_list = ServicesStatusesList

    def setup(self, application: web.Application) -> None:
        application.on_startup.append(self._on_connect)
        application.on_cleanup.append(self._on_disconnect)

    async def _on_connect(self, application: web.Application):
        self.config = application["config"]["postgres"]
        await self.gino.set_bind(self.config["database_url"])
        self.db = self.gino

    async def _on_disconnect(self, _) -> None:
        if self.db is not None:
            await self.db.pop_bind().close()

# alembic revision -m 'create table Message' --autogenerate