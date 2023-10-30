import asyncio

from fastapi import FastAPI
import uvicorn

from services.service_status import start_services_engine, services

app = FastAPI(title="Services_current_status")


@app.get(path="/start_services")
async def start_services():
    asyncio.create_task(start_services_engine())
    return "success"


@app.get(path="/current_status")
async def get_current_services_status():
    return services


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=8765)
