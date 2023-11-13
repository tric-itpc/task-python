<div id="header" align="center">
  <h1>StatusHistory</h1>
  <img src="https://img.shields.io/badge/Python-3.7.9-F8F8FF?style=for-the-badge&logo=python&logoColor=20B2AA">
  <img src="https://img.shields.io/badge/Django-3.2.23-F8F8FF?style=for-the-badge&logo=django&logoColor=00FF00">
  <img src="https://img.shields.io/badge/DjangoRestFramework-3.14.0-F8F8FF?style=for-the-badge&logo=django&logoColor=00FF00">
</div>


# Описание проекта:
Есть несколько рабочих сервисов, у каждого сервиса есть состояние работает/не работает/работает нестабильно.

Написан API который:

1. Получает и сохраняет данные сервиса: имя, состояние, описание.
2. Выводит список сервисов с актуальным состоянием.
3. По id сервиса выдает историю изменения состояния и все данные по каждому состоянию.
4. По указанному интервалу выдаёт информация о том сколько не работал сервис и считает SLA в процентах до 3-й запятой.

# Описание API:
- **GET /api/services/** - выводит список сервисов с актуальным состоянием.
- **POST /api/services/** - добавление нового сервиса.
- **GET /api/history/{service_id}/** - выдает историю изменений состояния.
- **GET /api/{service_id}/{start_date}/{end_date}/**: выдаёт информация о том сколько не работал сервис и считает SLA.

# Запуск проекта:
- Клонируйте репозиторий и перейдите в него.
- Установите и активируйте виртуальное окружение.
- Установите зависимости из файла requirements.txt
    ```
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ``` 
- Перейдите в папку **services** с файлом **manage.py**, выполните миграции, и запустите сервер:
    ```
    python manage.py migrate
    python manage.py runserver
    ```

После этого проект будет доступен по url-адресу [127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

Документация к API будет доступна по url-адресу [127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs/)