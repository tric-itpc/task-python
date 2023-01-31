from fastapi import FastAPI

from db import database
from resources.routes import api_router

app = FastAPI(
    title="API documentation",
    description="Реализация API из тестового задания",
    version="0.1.0",
)
app.include_router(api_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
