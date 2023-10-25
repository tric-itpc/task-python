

from classes.validation import service_model


def convert_to_service(dictionary: dict):
    id = str(dictionary.pop('_id'))
    return service_model(id=id, **dictionary)