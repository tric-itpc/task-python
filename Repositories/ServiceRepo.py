import datetime
import uuid

import pymongo

from db.db_connect import db
from model.service import Service


class ServiceRepo():

    @staticmethod
    async def get_all():
        _items = db.get_collection('service').find()
        _list_items = []
        async for item in _items:
            _list_items.append(item)
        return _list_items

    @staticmethod
    async def get_actual_state_service():
        _services = await db.service.distinct("name")
        _list_services = []
        for service in _services:
            actual_state = (db.get_collection('service').find({"name": service}).sort('state_dt', pymongo.DESCENDING)
                            .limit(1))
            _list_services.append(await actual_state.to_list(1))
        return _list_services

    @staticmethod
    async def get_state_data(state):
        _state = db.get_collection('service').find({"state": state}).sort('state_dt', pymongo.DESCENDING)
        _list_state = []
        async for state in _state:
            _list_state.append(state)
        return _list_state

    @staticmethod
    async def get_service_by_name(name):
        _service = db.get_collection('service').find({"name": name}).sort('state_dt', pymongo.DESCENDING)
        _list_service = []
        async for service in _service:
            _list_service.append(service)
        return _list_service

    @staticmethod
    async def get_sla(name, date_start, date_end):
        _service = (db.get_collection('service').find({"name": name, 'state_dt': {'$gt': date_start, '$lt': date_end}})
                    .sort('state_dt', pymongo.DESCENDING))
        downtime = datetime.timedelta()
        downtime_start = ''
        downtime_end = ''
        _list_state = []
        async for service in _service:
            _list_state.append(service)
            if service["state"] == "work":
                downtime_start = service["state_dt"]
                if not downtime_end == '':
                    downtime += downtime_end - downtime_start
                    downtime_start = ''
            if service["state"] == "nowork":
                downtime_end = service["state_dt"]
                if not downtime_start == '':
                    downtime += downtime_end - downtime_start
                    downtime_end = ''
        sla = ((date_end - date_start) - downtime) / (date_end - date_start) * 100
        return "{0:.0f} hours".format(downtime.total_seconds() // 3600), "{0:.3f}%".format(sla)

    @staticmethod
    async def insert(service: Service):
        id = str(uuid.uuid4())
        service.id = id
        _service = service.dict(exclude={})
        _service['_id'] = id
        _service.pop('id')
        await db.get_collection('service').insert_one(_service)
        return service

    @staticmethod
    async def delete_one(id: str):
        return await db.get_collection('service').delete_one({'_id': id})
