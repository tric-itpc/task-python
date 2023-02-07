import json
from bson import json_util
from datetime import datetime
from pymongo.errors import DuplicateKeyError


class ServicesStorage:

    def __new__(cls, db, *args, **kwargs):
        db.services.create_index('name', unique=True)

        return super().__new__(cls)

    def add(self, db, service):
        """add new service in db"""
        try:
            if service['current_status'] in [
                        'running', 'running unstable', 'stopping']:
                new_service = {
                    'name': service['name'],
                    'current_status': service['current_status'],
                    'statuses_history': [
                        {
                            'new_status': service['current_status'],
                            'description': service['description'],
                            'datetime_of_change': datetime.now()
                        }
                    ]
                    }
                try:
                    db.services.insert_one(new_service)
                except DuplicateKeyError:
                    return {'error': 'field name must be unique'}
            else:
                return {
                    'error':
                    'wrong status value'
                    }
        except KeyError:
            return {'error': 'wrong fields'}

        return json.loads(json_util.dumps(new_service))

    def update(self, db, name, new_status):
        """update service from db"""
        service = db.services.find_one({'name': name})
        try:
            if new_status[
                'new_status'] in [
                'running', 'running unstable', 'stopping'] and new_status[
                            'new_status'] != service['current_status']:
                if service['statuses_history'][-1]['new_status'] == 'stopping':
                    last_change_time = service[
                        'statuses_history'][-1]['datetime_of_change']
                    time_of_stopping = int(
                        (datetime.now() - last_change_time).total_seconds())
                    change_of_status = {
                        'new_status': new_status['new_status'],
                        'description': new_status['description'],
                        'datetime_of_change': datetime.now(),
                        'time_of_stopping': time_of_stopping
                    }
                else:
                    change_of_status = {
                        'new_status': new_status['new_status'],
                        'description': new_status['description'],
                        'datetime_of_change': datetime.now()
                    }
                try:
                    db.services.update_one(
                        {'_id': service['_id']},
                        {'$set': {'current_status': new_status['new_status']}}
                    )
                    db.services.update_one(
                        {'_id': service['_id']},
                        {'$push': {'statuses_history': change_of_status}}
                    )
                except TypeError:
                    return {
                        'error': f'document with name {name} doesn`t exist'}
            else:
                return {'error':
                        'wrong status value'
                        }
        except KeyError:
            return {'error': 'wrong fields'}

        updated_service = db.services.find_one({'name': name})

        return json.loads(json_util.dumps(updated_service))

    def get_all(self, db):
        """get all services in format {_id, name, status}"""
        all_services = db.services.find({}, {'statuses_history': 0})
        print(db.services.index_information())

        return json.loads(json_util.dumps(all_services))

    def get_service_history(self, db, name):
        """get history of service's statuses"""
        service = db.services.find_one({'name': name}, {'statuses_history': 1})
        if not service:
            return {'error': f'document with name {name} doesn`t exist'}

        return json.loads(json_util.dumps(service))

    def delete(self, db, name):
        """delete service from db"""
        service = db.services.find_one({'name': name})
        if not service:
            return {'error': f'document with name {name} doesn`t exist'}
        db.services.delete_one(service)

        return {'status': 'service was deleted'}

    def get_sla(self, db, name):
        """get service's sla"""
        service = db.services.find_one({'name': name})
        working_time = int(
            (
                datetime.now() - service[
                                 'statuses_history'][0][
                                 'datetime_of_change']).total_seconds()
            )
        aggregate = db.services.aggregate([
            {
                '$match': {
                    'name': name
                }
            }, {
                '$unwind': {
                    'path': '$statuses_history'
                }
            }, {
                '$unwind': {
                    'path': '$statuses_history.time_of_stopping'
                }
            }, {
                '$group': {
                    '_id': 'time_of_stopping',
                    'time_of_stopping': {
                        '$sum': '$statuses_history.time_of_stopping'
                    }
                }
            }
        ])

        result = next(aggregate, None)
        if result:
            time_of_stopping = result['time_of_stopping']
            sla = round(float(100 - (time_of_stopping/working_time) * 100), 3)
            return {'SLA': f'{sla}%'}
        else:
            return {'SLA': '100%'}
