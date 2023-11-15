# API контроля за сервисами

## Описание

API написан на Django, база данных возводится в контейнере (postgres и pgadmin в docker-compose). Возможен вариант написания API во Flask или FastAPI

### Функционал API

- Получает и сохраняет данные: имя, состояние, описание
- Выводит список сервисов с актуальным состоянием
- По имени сервиса выдает историю изменения состояния и все данные по каждому состоянию

## Примеры запросов 

- Располагаются в файле /requests-examples.http

## Установка и запуск в тестовом формате

- pip install -r requirements.txt
- docker-compose up
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver 0.0.0.0:8000
