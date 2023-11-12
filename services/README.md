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
- **POST /api/services/** - Добавление нового сервиса.
- **GET /api/history/{id_сервиса}/** - выдает историю изменения состояния.
- **GET /api/{id_сервиса}/{start_date}/{end_date}/**: выдаёт информация о том сколько не работал сервис и считает SLA.
```
url: /api/4/2023-10-29/2023-11-13/
Response: [
    {
        "Информация для сервиса": "Fourth",
        "Service level agreement(в процентах)": 96.913,
        "Общее время недоступности сервиса(в секундах)": "5334.910411"
    }
]
```

Выполнил Конышкин Иван