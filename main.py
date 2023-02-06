from fastapi import FastAPI
from db import DB
from status import status

app = FastAPI()
db = DB()


# Добавляет новый сервис в список
@app.post("/new/{service}")
async def new_service(service):
    if service not in db.service_list():
        db.add_service(service)
        db.update_services(status([service]))


# Удаляет сервис из списка
@app.delete("/del/{service}")
async def delete_service(service):
    if service in db.service_list():
        db.delete_service(service)


# Выводит список сервисов с актуальным состоянием и добавляет информацию в базу данных
@app.get("/status")
async def read_status():
    state = status(db.service_list())
    db.update_services(state)
    return {i: state[i]["description"] for i in state}


# Показывает актуальное состояние сервиса и обновляет информацию в базе данных
@app.get("/{service}")
async def status_service(service):
    if service in db.service_list():
        state = status([service])
        db.update_services(state)
        return {i: state[i]["description"] for i in state}


# По имени сервиса выдает историю изменения состояния и все данные по каждому состоянию
@app.get("/story/{service}")
async def read_item(service):
    return db.story_status(service)

