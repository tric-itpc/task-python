import requests


def status(services):
    state = {}
    for service in services:
        state[service] = {}
        if not service.startswith('http'):
            url = 'http://'+service
        else:
            url = service
        res = requests.get(url=url)
        state[service]["code"] = str(res.status_code)
        if res.status_code // 100 == 2:
            state[service]["description"] = "Работает"
        elif res.status_code // 100 == 5:
            state[service]["description"] = "Не работает"
        else:
            state[service]["description"] = "Ошибка " + str(res.status_code)
    return state
