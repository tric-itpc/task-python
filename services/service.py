from fastapi import HTTPException
from models.service import Service, ServiceHistory
from datetime import datetime
from sqlalchemy.orm import Session
from schemas import service
import dateutil.parser as parser
from utils import calc_sum_downtime, calc_downtime
def create_service(data: service.Service, db): # создание сервиса
    service = Service(name=data.name, state=data.state, description=data.description)

    service_object = db.query(Service).filter(Service.name == data.name.capitalize()).first()
    if service_object:
        raise HTTPException(status_code=400,
                            detail='Такой сервис уже в базе')
    try:
        db.add(service)
        db.commit()
        db.refresh(service)

    except Exception as e:
        print(e)

    serviceHistory = ServiceHistory(service_name=service.name, from_state=None, to_state=data.state,
                                     change_time=datetime.now()) # добавление изменения состояния
    try:
        db.add(serviceHistory)
        db.commit()
        db.refresh(serviceHistory)

    except Exception as e:
        print(e)

    return service


def get_service(db): #получение всех сервисов
    return db.query(Service).all()


def update_service(data: service.Service, db: Session, name: str): #обновление сервиса
    service = db.query(Service).filter(Service.name == name).first()

    service_object = db.query(Service).filter(Service.name == data.name.capitalize()).first()
    if service_object is None:
        raise HTTPException(status_code=400,
                            detail='Такого сервиса нет в базе')


    serviceHist = db.query(ServiceHistory).filter(ServiceHistory.service_name == name).order_by(ServiceHistory.id.desc()).first()
    if service.state != data.state:
        serviceHistory = ServiceHistory(service_name=service.name, from_state=service.state, to_state=data.state, change_time=datetime.now(),
                                         time_not_working = calc_downtime(service.state, data.state, serviceHist.change_time))
        try:
            db.add(serviceHistory)
            db.commit()
            db.refresh(serviceHistory)

        except Exception as e:
            print(e)
    service.name = data.name
    service.state = data.state
    service.description = data.description
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def get_services_by_state(state: str, db: Session):
    return db.query(Service).filter(Service.state == state).all()


def get_service_history(name: str, db: Session): # все изменения состояния сервиса
    return db.query(ServiceHistory).filter(ServiceHistory.service_name == name).all()

def calculate_sla(name: str, db: Session, start:str, end:str): #рассчет sla(костыльно - переписать)

    service_object = db.query(Service).filter(Service.name == name.capitalize()).first()
    if service_object is None:
        raise HTTPException(status_code=400,
                            detail='Такого сервиса нет в базе')


    service_object = db.query(Service).filter(Service.name == name.capitalize()).first()
    if service_object is None:
        raise HTTPException(status_code=400,
                            detail='Такого сервиса нет в базе')

    if end<start:
        raise HTTPException(status_code=400,
                            detail='Неверный временной отрезок')

    histories = db.query(ServiceHistory).filter(ServiceHistory.service_name == name)\
        .filter(ServiceHistory.change_time>parser.parse(start)).filter(ServiceHistory.change_time < parser.parse(end)).all()
    all_time = db.query(ServiceHistory).filter(ServiceHistory.service_name == name).all()
    sum_not_stable, downtimes_by_period = calc_sum_downtime(histories)
    sum_not_stable2, all_downtimes = calc_sum_downtime(all_time)
    if all_downtimes != 0:
        s = (sum_not_stable2.total_seconds() - sum_not_stable.total_seconds()) / sum_not_stable2.total_seconds() * 100
    else:
        s = 100



    return {'service_name': name,
            'from_date': parser.parse(start),
            'to_date': parser.parse(end),
            "SLA": round(s, 3),
            "all_downtimes": all_downtimes,
            "downtimes_by_period": downtimes_by_period,
            }

