from constants import ServiceStates

import json
from datetime import datetime, date
from dataclasses import dataclass
import datetime as dt


@dataclass
class State:
    work_state: ServiceStates
    description: str
    time: datetime = datetime.now()

    @property
    def get_state_value(self):
        return self.work_state.value

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def to_dict(self):
        return {
            'state': f'{self.get_state_value}',
            'description': f'{self.description}',
            'time': f'{self.time.isoformat(" ", "seconds")}'
        }

    @staticmethod
    def state_from_json(json_str):
        json_dict = json.loads(json_str)
        if {'state', 'description'}.issubset(json_dict.keys()):
            if 'time' in json_dict:
                return State(ServiceStates(json_dict['state']), json_dict['description'],
                             datetime.strptime(json_dict['time'], '%Y-%m-%d %H:%M:%S'))
            return State(ServiceStates(json_dict['state']), json_dict['description'])
        raise KeyError(f'JSON must have following keys: state, description, time')


@dataclass
class Service:
    name: str
    state: State

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def to_dict(self):
        return {
            'name': f'{self.name}',
            'state': f'{self.state.to_dict()}'
        }

    @staticmethod
    def service_from_json(json_str):
        json_dict = json.loads(json_str)
        state = State.state_from_json(json_str)
        if {'name'}.issubset(json_dict.keys()):
            return Service(json_dict['name'], state)
        raise KeyError(f'JSON must have following keys: name')


class DateInterval:
    def __init__(self, start_date, end_date, work_state):
        self.right = None
        self.left = None
        if not isinstance(start_date, (datetime, date)) and isinstance(end_date, (datetime, date)):
            raise TypeError(f'{start_date} and {end_date} should be date or datetime')
        self.start = start_date
        self.end = end_date
        self.work_state = work_state

    def in_interval(self,date_time):
        return self.start <= date_time <= self.end

    def split_interval(self, state):
        if not self.in_interval(state.time):
            raise ValueError(f'{state.time} was outside the bounds of the interval')
        if self.left is None and self.right is None:
            self.left = DateInterval(self.start, state.time, self.work_state)
            self.right = DateInterval(state.time, self.end, state.work_state)
        else:
            if state.time <= self.left.end:
                self.left.split_interval(state)
            else:
                self.right.split_interval(state)

    def calculate_states_time(self):
        intervals_stack = [self]
        times = {
            ServiceStates.WORKS: 0,
            ServiceStates.NOT_WORKS: 0,
            ServiceStates.WORKS_UNSTABLE: 0
        }
        while len(intervals_stack) > 0:
            current_interval = intervals_stack.pop()
            if current_interval.left is None and current_interval.right is None:
                times[current_interval.work_state] += (current_interval.end - current_interval.start).total_seconds()
            else:
                intervals_stack.append(current_interval.left)
                intervals_stack.append(current_interval.right)
        return times
