from django.core.exceptions import ValidationError
from django.db import models


class Services(models.Model):
    name = models.CharField(
        verbose_name='Название сервиса',
        max_length=200,
        unique=True,
    )

    description = models.TextField(
        verbose_name='Описание', max_length=350,
        blank=True, null=True)

    def __str__(self):
        return self.name


class TimeStamps(models.Model):
    STATUSES = ('working', 'unstable', 'down')
    CHOICES = [(s, s) for s in STATUSES]

    time_stamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    service = models.ForeignKey(
        Services,
        on_delete=models.SET_NULL,
        related_name='timestamps',
        null=True
        )
    status = models.CharField(
        verbose_name='Состояние сервиса',
        choices=CHOICES,
        blank=False,
        max_length=30,
        )
    description = models.TextField(
        verbose_name='Описание', max_length=350,
        blank=True, null=True)

    def clean(self):
        if self.status not in self.STATUSES:
            raise ValidationError('Указано недопустимое значение статуса')
        return super().clean()
