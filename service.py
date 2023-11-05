import json
import datetime as dt
from structures import DateInterval, Service, State
from constants import ServiceStates as st


class ServiceChecker:
    def __init__(self):
        self.json_db_path = 'services.json'

    def get_services(self):
        with open(self.json_db_path, 'r', encoding='utf-8') as db:
            data = json.load(db)
        services = []
        for service in data['services']:
            current_state = max(
                list(
                    map(lambda x: State.state_from_json(json.dumps(x)), service['history'])
                ), key=lambda x: x.time
            )
            services.append({
                "name": service['name'],
                "state": current_state.get_state_value
            })
        return str(services)

    def get_service_history(self, name):
        with open(self.json_db_path, 'r', encoding='utf-8') as db:
            for service in json.load(db)['services']:
                if name == service['name']:
                    return str(service['history'])
            raise KeyError(f'service {name} does not exist')

    def add_service(self, service_json):
        service = Service.service_from_json(service_json)
        with open(self.json_db_path, 'r', encoding='utf-8') as db:
            services = json.load(db)['services']

        if service.name not in list(map(lambda x: x['name'], services)):
            services.append({'name': service.name, 'history': []})

        service_dict = next(s for s in services if s['name'] == service.name)
        service_dict['history'].append(service.state.to_dict())

        with open(self.json_db_path, 'w', encoding='utf-8') as db:
            json.dump({'services': [s for s in services]}, db, ensure_ascii=False, )

    def SLA(self, start_time, end_time):
        result = []

        with open(self.json_db_path, 'r', encoding='utf-8') as db:
            services_with_history = json.load(db)['services']

        for service in services_with_history:
            begin_state = State(st.NOT_WORKS, '', start_time + dt.timedelta(days=1))
            interval = DateInterval(start_time, end_time, begin_state.work_state)
            for state_json in service['history']:
                state = State.state_from_json(json.dumps(state_json, ensure_ascii=False))
                if interval.in_interval(state.time):
                    interval.split_interval(state)
                if state.time <= start_time:
                    if begin_state.time <= start_time:
                        begin_state = state if state.time > begin_state.time else begin_state
                    else:
                        begin_state = state

            left_interval = interval
            while left_interval.left is not None:
                left_interval = left_interval.left

            if begin_state != start_time + dt.timedelta(days=1):
                left_interval.work_state = begin_state.work_state

            times = interval.calculate_states_time()
            service_sla = {
                'name': service['name'],
                'SLA': 0
            }
            if times[st.WORKS] != 0 and (times[st.WORKS] - times[st.NOT_WORKS]) > 0:
                service_sla['SLA'] = round((times[st.WORKS] - times[st.NOT_WORKS]) / times[st.WORKS], 3) * 100
            result.append(service_sla)
        return str(result)
