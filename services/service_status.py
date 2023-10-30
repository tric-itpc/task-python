import asyncio

from random import randint, choice


services = {
    "celery": "stable",
    "redis": "stable",
    "postgres": "stable",
    "openvpn": "stable",
}


def counting_probability_of_status_change() -> str:
    number = randint(0, 100)

    if number > 90:
        return "out_of_service"
    if number > 60:
        return "unstable"

    return "stable"


async def start_services_engine():
    while True:
        interval = randint(1, 2)
        status = counting_probability_of_status_change()
        service_name = choice(list(services.keys()))
        await asyncio.sleep(interval)
        services[service_name] = status
        print(services)


