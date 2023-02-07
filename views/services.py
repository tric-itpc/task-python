from flask import Blueprint, request
from database.storage import ServicesStorage
from database.db import db

storage = ServicesStorage(db)

routes = Blueprint('services', __name__)


@routes.post('/')
def add():
    payload = request.json

    return storage.add(db, payload)


@routes.put('/<name>')
def update_status(name):
    payload = request.json

    return storage.update(db, name, payload)


@routes.get('/')
def get_all_services():
    return storage.get_all(db)


@routes.get('/<name>')
def get_service_by_name(name):
    return storage.get_service_history(db, name)


@routes.delete('/<name>')
def delete(name):
    return storage.delete(db, name)


@routes.get('/<name>/sla')
def get_sla(name):
    return storage.get_sla(db, name)
