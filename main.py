from fastapi import FastAPI
from routers import service


app = FastAPI()
app.include_router(service.router)
