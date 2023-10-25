from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple, Union

from classes.enums import Status
from classes.validation import sla_object


class IRepository(ABC):
    @abstractmethod
    def get(self, **kwargs) -> List[Any]:
        """
        Returns a list of querying objects.
        kwargs: other parameters used to filter by the specified fields
        """
        pass

    @abstractmethod
    def add(self, element: dict) -> str:
        """
        Returns an ObjectID of inserted element as a string format
        element: dictionary representation of the inserted element
        """
        pass

    # @abstractmethod
    # def update(self, id: str, element: dict) -> dict:
    #     """
    #     Returns a dictionary representation of the old element
    #     id: ObjectID of updated element
    #     element: dictionary representation of the updated element
    #     """
    #     pass

    @abstractmethod
    def remove(self, **kwargs) -> int:
        """
        Returns the count of deleted elements
        kwargs: parameters used to filter by the special fields
        """
        pass


class IStatisticService(ABC):
    @abstractmethod
    def set_collection(self, collection: list) -> None:
        pass

    @abstractmethod
    def set_interval(self, start: datetime, end: datetime) -> None:
        pass

    @abstractmethod
    def summary_time_by_status(self, status: Status) -> float:
        pass

    @abstractmethod
    def sla_calculate(
        self,
        total_time: float,
        disable_time: float,
        unstable_time: float,
    ) -> Tuple[float, float]:
        pass