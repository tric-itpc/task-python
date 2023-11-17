import datetime
import uuid
import pymongo

from db.db_connect import db
from model.service import Service


STATE_WORK = 'work'
STATE_NOT_WORK = 'notwork'


class ServiceRepo():

    @staticmethod
    async def get_all():
        """ Выводит список сервисов """
        items = db.get_collection('service').find()
        list_items = []
        async for item in items:
            list_items.append(item)
        return list_items

    @staticmethod
    async def get_actual_state_service():
        """ Выводит список сервисов с актуальным состоянием """

        services = await db.service.distinct('name')
        list_services = []
        for service in services:
            actual_state = (
                db.get_collection('service')
                .find({'name': service})
                .sort('state_dt', pymongo.DESCENDING)
                .limit(1)
            )
            list_services.append(await actual_state.to_list(1))
        return list_services

    @staticmethod
    async def get_state_data(state: str):
        """ Dсе данные по каждому состоянию """

        states = (
            db.get_collection('service')
            .find({'state': state})
            .sort('state_dt', pymongo.DESCENDING)
        )
        list_state = []
        async for state in states:
            list_state.append(state)
        return list_state

    @staticmethod
    async def get_service_by_name(name: str):
        """ По имени сервиса выдает историю изменения состояния """

        services = (
            db.get_collection('service')
            .find({'name': name})
            .sort('state_dt', pymongo.DESCENDING)
        )
        list_service = []
        async for service in services:
            list_service.append(service)
        return list_service

    @staticmethod
    async def get_sla(name: str, date_start: datetime.datetime, date_end: datetime.datetime):
        """ По указанному интервалу выдается информация о том сколько не работал сервис и считает SLA """

        services = (
            db.get_collection('service')
            .find({'name': name, 'state_dt': {'$gt': date_start, '$lt': date_end}})
            .sort('state_dt', pymongo.DESCENDING)
        )
        previous_service = (
            db.get_collection('service')
            .find({'name': name, 'state_dt': {'$lt': date_start}})
            .sort('state_dt', pymongo.DESCENDING)
            .limit(1)
        )
        list_state = []
        downtime = datetime.timedelta()
        downtime_end = None
        downtime_start = None

        async for service in previous_service:
            if service['state'] == STATE_NOT_WORK:
                list_state.append(service)

        async for service in services:
            if service['state'] == STATE_NOT_WORK:
                downtime_start = service['state_dt']
                if downtime_end:
                    downtime += downtime_end - downtime_start
                    downtime_end = None
                    continue
                downtime += date_end - downtime_start
            elif service['state'] == STATE_WORK:
                downtime_end = service['state_dt']

        if list_state and downtime_end:
            downtime += downtime_end - date_start
            list_state.pop()
        elif list_state and downtime_start:
            downtime += downtime_start - date_start
            list_state.pop()

        sla = get_formatted_sla(date_start, date_end, downtime)
        return sla


    @staticmethod
    async def insert(service: Service):
        """ Получает и сохраняет данные: имя, состояние, описание """

        id = str(uuid.uuid4())
        service.id = id
        service = service.dict(exclude={})
        service['_id'] = id
        service.pop('id')
        await db.get_collection('service').insert_one(service)
        return service

    @staticmethod
    async def delete_one(id: str):
        """ Удаление сервиса """

        return await db.get_collection('service').delete_one({'_id': id})


def get_formatted_sla(date_start: datetime.datetime, date_end: datetime.datetime, downtime: datetime.timedelta):
    """ Форматирование строки SLA """

    sla = ((date_end - date_start) - downtime) / (date_end - date_start) * 100
    return '{0:.0f} hours'.format(downtime.total_seconds() // 3600), '{0:.3f}%'.format(sla)
