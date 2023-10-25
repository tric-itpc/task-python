from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.service import service_router
from settings import env

app = FastAPI()

app.include_router(service_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[env.SERVER_ORIGIN],
    allow_credentials=True,
    allow_methods=[env.SERVER_METHOD],
    allow_headers=[env.SERVER_HEADER],
)


@app.get("/")
async def root():
    return {"to view the documentation use": "/docs or /redoc"}