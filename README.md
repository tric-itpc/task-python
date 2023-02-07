# API-сервис

Реализован на Flask, данные о сервисах хранятся в MongoDB.

Реализована возможность добавить сервис в базу данных, изменить его статус или удалить сервис из БД.

Роуты могут вывести список сервисов (имя – текущий статус), историю измений статусов конкретного сервиса или SLA.

SLA рассчитывается как процент времени, что сервис имел статус «работает» или «работает нестабильно» от общего количества времени, что сервис находился в БД.

Все имена сервисов в MongoDB имеют уникальные значения.

Задать статусу можно только значение «running», «running unstable» или «stopping». При изменении статуса нужно не просто указать один из этих трех – новый статус должен отличаться от предыдущего.

Все данные выводятся в JSON.