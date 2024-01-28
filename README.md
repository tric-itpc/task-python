# Python TEST TASK for itpc.ru
Этот проект представляет собой API, которое позволяет выполнять следующие действия:

    - Сохранение данных: API принимает данные, включая имя сервиса, его текущее состояние и описание, и сохраняет их в базе данных.
    - Вывод списка сервисов с актуальным состоянием: API предоставляет эндпоинт для получения списка сервисов с их текущим состоянием.
    - История изменения состояния: По имени сервиса API позволяет получать историю изменения состояния и всю доступную информацию по каждому состоянию сервиса.

## Ресурсы
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLalchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [PostgreSQL](https://www.postgresql.org/)


## Документация
Установка зависимостей:
```
pip install -r reuirements.txt
```
Запуск через main.py, либо через консоль:
```
uvicorn main:app --reload
```


После запуска документация доступна по адресу http://127.0.0.1:8000/docs/
Реализовано через OpenAPI(Swagger)
