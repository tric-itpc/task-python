from aiohttp import web

import asyncio
from app.routes import setup_routes

from utils.database.accessor import PostgresAccessor

def setup_config(application):
   from settings import config
   application["config"] = config

async def setup_on_startup(application):
   await application['db']._on_connect(application)
   # await application['monitor']._on_connect(application)

async def setup_on_disconnect(application):
   await application['db']._on_disconnect(application)
   # await application['monitor']._on_disconnect(application)

def setup_app(application):
   setup_config(application)
   application['db'] = PostgresAccessor()
   # application['monitor'] = ServicesMonitor()
   application.on_startup.append(setup_on_startup)
   application.on_cleanup.append(setup_on_disconnect)
   application['monitoring'] = False
   setup_routes(application)


app = web.Application()

if __name__ == "__main__":
   setup_app(app)
   web.run_app(app)