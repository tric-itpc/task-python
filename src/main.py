from fastapi import FastAPI

from src.routers.service_status import router

app = FastAPI()

app.include_router(router)