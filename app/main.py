import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import routes
from app.database import DbConnector
from app.settings import settings

app = FastAPI(title=f'{settings.TITLE_API}', docs_url=settings.DOC_URL, VERSION=settings.VERSION)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(routes.router)


@app.on_event('startup')
async def startup_event():
    database = DbConnector()
    if settings.DROP_DATABASE:
        await database.drop_tables()
    await database.create_tables()


if __name__ == '__main__':
    uvicorn.run('main:app', port=settings.SERVER_PORT)
