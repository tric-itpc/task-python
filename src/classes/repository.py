from typing import Dict, List, Union

from pymongo.collection import Collection, ReturnDocument

from classes.helper import convert_to_service
from classes.interfaces import IRepository
from settings import env


class ServiceRepository(IRepository):
    def __init__(self, collection: Collection) -> None:
        self.db = collection

    def get(self, **kwargs) -> List[Dict]:
        filter = kwargs
        cursor = self.db.find(filter)
        return [convert_to_service(doc) for doc in cursor]

    def add(self, element: dict) -> str:
        result = self.db.insert_one(element)
        return str(result.inserted_id)

    # def update(self, id: str, element: dict) -> dict:
    #     filter = {env.PARAM_ID: id}
    #     update = {"$set": element}

    #     old_element = self.db.find_one_and_update(
    #         filter=filter, update=update, return_document=ReturnDocument.BEFORE
    #     )
    #     return old_element

    def remove(self, **kwargs) -> int:
        filter = kwargs
        result = self.db.delete_many(filter)
        return result.deleted_count