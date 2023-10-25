from copy import deepcopy
from datetime import datetime, timedelta
from typing import List, Tuple

from classes.enums import Status
from classes.validation import difference_model, service_model
from settings import env


class StatisticService:
    def __init__(self) -> None:
        self.collection = [dict]
        self.start = None
        self.end = None

    def set_collection(self, collection) -> None:
        self.collection = collection

    def set_interval(self, start: datetime, end: datetime) -> None:
        self.start = start
        self.end = end

    def summary_time_by_status(self, status: Status) -> float:
        if self.collection == [] or self.start == None and self.end == None:
            return 0.0

        elems = sorted(self.collection, key=lambda item: item.date_time)

        times: List[timedelta] = []

        def calc_difference(current: datetime, next: datetime) -> timedelta:
            def interval_check(date_time: datetime, cmp: str, deadline: datetime):
                return (
                    date_time if date_time.__getattribute__(cmp)(deadline) else deadline
                )

            early = interval_check(current, "__ge__", self.start)
            later = interval_check(next, "__le__", self.end)
            if early > later:
                return timedelta()
            return later - early

        def exist_at(l: list, index: int) -> bool:
            try:
                return bool(l[index])
            except IndexError:
                return bool(None)

        for i in range(len(elems)):
            if elems[i].status != status.value:
                continue
            if i == 0 and (not exist_at(elems, i + 1)) or i == len(elems) - 1:
                times.append(calc_difference(elems[i].date_time, datetime.now()))
                continue
            if i == 0 and exist_at(elems, i + 1) or i < len(elems) - 1:
                times.append(
                    calc_difference(elems[i].date_time, elems[i + 1].date_time)
                )

        return sum(map(lambda item: item.total_seconds(), times))

    def sla_calculate(
        self,
        total_time: float,
        disable_time: float,
        unstable_time: float,
    ) -> Tuple[float, float]:
        if total_time == 0:
            return 0.0, 0.0
        return (
            round((total_time - (disable_time + unstable_time)) / total_time * 100, 3),
            round((total_time - disable_time) / total_time * 100, 3),
        )