import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import routers
from database import get_db
from settings import settings


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(routers.router)


@app.on_event('startup')
async def startup_event():
    database = get_db()
    if settings.DROP_DATABASE:
        await database.drop_tables()
    await database.create_tables()


if __name__ == '__main__':

    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)