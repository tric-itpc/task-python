# Python TEST TASK for itpc.ru
Этот проект представляет собой API, которое позволяет выполнять следующие действия:

    Сохранение данных: API принимает данные, включая имя сервиса, его текущее состояние и описание, и сохраняет их в базе данных.

    Вывод списка сервисов с актуальным состоянием: API предоставляет эндпоинт для получения списка сервисов с их текущим состоянием.

    История изменения состояния: По имени сервиса API позволяет получать историю изменения состояния и всю доступную информацию по каждому состоянию сервиса.

## Содержание
- [Технологии](#технологии)
- [Использование](#использование)
- [Документация](#документация)
- [To do](#to-do)
- [Команда проекта](#команда-проекта)

## Технологии
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLalchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [OpenAPI](https://www.openapis.org/)


## Использование
Расскажите как установить и использовать ваш проект, покажите пример кода:

Склонируйте репоизиторий на локальную машину:
```sh
$ git clone https://github.com/advatroniks/task-python
```

Перейдите в папку с проектом:
```sh
$ cd /task-python
```

Выполнитье команды Docker.
```docker
$ sudo docker compose up
```
## Документация
После запуска документация доступна по адресу http://127.0.0.1:8080/docs#/
Реализовано через OpenAPI(Swagger)

## To do
- [x] Основной функционал
- [ ] SLA task


## Команда проекта
- [Advatrnoiks](t.me/advatroniks) tixxx333@yandex.ru — Back-End Engineer
