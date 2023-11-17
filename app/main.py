from fastapi import FastAPI
from sqlalchemy import desc
from database import Session, Service, StateHistory
from fastapi.responses import JSONResponse
import json
import random
import constants
from datetime import datetime

app = FastAPI()


@app.get("/save_service/")
def save_service():
    """получение и сохранение сервиса в бд"""
    random_service = random.choice(constants.SERVISES['services'])  # имитация сервисов
    random_service["state"] = random.choice(list(constants.SERVICE_STATUS.values()))  # имитация состояний сервисов

    cur_session = Session()
    service_obj = Service()

    if cur_session.query(Service).filter(Service.name == random_service["name"]).first():
        cur_session.query(Service).filter(Service.name == random_service['name']).update(
            {
                Service.state: random_service["state"],
                Service.saved_at: datetime.now()
            }
        )
    else:
        service_obj.name = random_service["name"]
        service_obj.state = random_service["state"]
        service_obj.description = random_service["description"]
        cur_session.add(service_obj)

    cur_session.commit()
    change_state(cur_session.query(Service).filter(Service.name == random_service["name"]).first())
    return random_service


def change_state(service_data):
    session = Session()
    history_obj = StateHistory()

    history_obj.service_name = service_data.name
    history_obj.state = service_data.state
    history_obj.updated_at = datetime.now()
    if service_data.state == "не работает":  # если сервис не работает, сразу устанавливаем время начала простоя
        history_obj.downtime = service_data.saved_at

    last_state = session.query(StateHistory).order_by(desc(StateHistory.updated_at)).filter(
        StateHistory.service_name == service_data.name).first()  # смотрим последний сохранённый статус сервиса

    if last_state is not None:
        if service_data.state != last_state.state:
            if last_state.state == "не работает":
                session.query(StateHistory).filter(
                    StateHistory.id == last_state.id).update(
                    {
                        StateHistory.uptime: service_data.saved_at,
                        StateHistory.updated_at: datetime.now()
                    }
                )
            session.add(history_obj)
    else:
        session.add(history_obj)

    session.commit()


@app.get("/get_services/")
def get_services():
    session = Session()
    services = session.query(Service).all()
    result = []
    for service in services:
        result.append({
            'name': service.name,
            'state': service.state,
            'description': service.description,
            'saved_at': f'{service.saved_at}'
        })
    return JSONResponse({'services': result})


@app.post("/get_state_history/")
def get_state_history(service_n):
    session = Session()
    history = session.query(StateHistory).filter(StateHistory.service_name==service_n).all()
    result = []
    for hi in history:
        result.append(
            {
                'state': hi.state,
                'updated_at': f'{hi.updated_at}',
                'downtime': f'{hi.downtime}',
                'uptime': f'{hi.uptime}'
            }
        )
    return JSONResponse({'history': result})

