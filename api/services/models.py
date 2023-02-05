from django.db import models


class Service(models.Model):
    """Модель сервиса. По условиям тестового задания, сервисы уже существуют,
    поэтому добавление сервисов реализовано только через панель администратора"""

    name = models.SlugField(
        verbose_name='Имя сервиса',
    )

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

    def __str__(self):
        return self.name


class Status(models.Model):
    """Модель состояния. По условиям тестового задания, состояния фиксированы,
    поэтому добавление статусов реализовано только через панель администратора"""

    name = models.SlugField(verbose_name='Статус')

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name


class ServiceStatus(models.Model):
    """Модель сервис-статус. Для хранения информации
    о состоянии сервиса в определенный момент времени"""

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='status',
        verbose_name='Сервис',
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name='service',
        verbose_name='Статус',
    )
    description = models.TextField(
        verbose_name='Текстовое описание состояния',
    )
    date_time = models.DateTimeField(
        verbose_name='Дата обновления состояния',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Cтатус сервиса'
        verbose_name_plural = 'Статусы сервисов'

    def __str__(self):
        return f'{self.service} - {self.status}'
