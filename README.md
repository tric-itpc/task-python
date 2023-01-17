# Вакансия :: Программист Python

Разработка бизнес-системы с использованием веб-технологий Автоматизация сервисов с большим количеством пользователей

## От вас

### Обязательно

- Знание синтаксиса языка Python
- Опыт разработки на Python не менее 1 года
- Базовые знания принципов работы Web
- Желание работать в команде и развиваться

### Приветствуется

- Навыки работы с Flask, Sanic
- Опыт работы с БД: PostgreSQL, MS SQL, MongoDB
- Опыт разработки под ОС семейства GNU Linux
- Работа с системами управления исходным кодом Git
- Знания базовых принципов разработки (тестирование, рефакторинг, Code Review)

### Будет круто, но не обязательно

- Знание английского языка на уровне чтения технической документации
- Участие в разработке Open Source проектов
- Наличие профиля на GitHub, Stack Overflow
- Наличие проектов которые можете продемонстрировать
- Разработка с использованием TypeScript, знание современных frontend-бибилотек и подходов к разработке

## У нас

- Полный рабочий день, гибкий обед по желанию сотрудника, гибкое время начала рабочего дня
- Полностью «белая» заработная плата с возможностью увеличения в процессе работы (зависит от отдачи сотрудника)
- Добровольное медицинское страхование
- Дружелюбная команда с юмором, готовая поддержать
- Возможность одновременно участвовать в разных проектах и развивать другие компетенции (JS и все модное)
- Полностью «белая» заработная плата с возможностью увеличения в процессе работы (зависит от отдачи сотрудника)
- По желанию: один день в неделю - удаленная работа
- Никаких опенспейсов, а комфортное пространство в центре Тюмени
- Готовы безгранично делиться опытом при условии, что вы готовы принимать

Если у вас есть опыт работы с 1С, то эта вакансия не для вас. Даже не пытайтесь. Если вакансия вас заинтересовала, но есть какие-то недопонимания и вопросы, приходите, обсудим, договоримся.   
Большим плюсом будет решение тестового задания. Решение принимается в виде PR к текущему проекту 

## Тестовое задание

Есть несколько рабочих сервисов, у каждого сервиса есть состояние работает/не работает/работает нестабильно.

Требуется написать API который:
1. Получает и сохраняет данные.
  - имя
  - состояние
  - описание
2. Выводит список сервисов с актуальным состоянием
3. По имени сервиса выдает историю изменения состояния и все данные по каждому состоянию

Дополнительным плюсом будет 
1. По указанному интервалу выдается информация о том сколько не работал сервис и считать SLA в процентах до 3-й запятой

Вывод всех данных должен быть в формате JSON