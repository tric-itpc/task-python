from django.db import models
from django.utils import timezone

tz = timezone.get_default_timezone()


class Service(models.Model):
    """Модель для сервисов."""

    IS_STABLE = 'работает'
    NOT_WORKING = 'не работает'
    INSTABILITY = 'нестабильно'
    STATUSES = [
        (IS_STABLE, 'работает'),
        (NOT_WORKING, 'не работает'),
        ('нестабильно', 'нестабильно')
    ]
    name = models.CharField(
        max_length=100, unique=True,
        verbose_name='Название'
    )
    status = models.CharField(
        max_length=50, verbose_name='Состояние',
        choices=STATUSES, default='работает'
    )
    description = models.TextField(verbose_name='Описание')

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name


class StatusHistory(models.Model):
    """Модель для хранения истории изменений состояния работы сервиса."""

    status = models.CharField(max_length=50, verbose_name='Состояние')
    service = models.ForeignKey(
        Service, related_name='history',
        verbose_name='Название', on_delete=models.CASCADE
    )
    last_modified = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата изменения'
    )
    start_time = models.DateTimeField(
        null=True, blank=True,
        verbose_name='Время начала недоступности сервиса'
    )
    end_time = models.DateTimeField(
        null=True, blank=True,
        verbose_name='Время окончания недоступности сервиса'
    )

    @property
    def downtime_duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        elif not self.end_time and self.start_time:
            return timezone.now() - self.start_time
        return None

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'Изменение сервиса "{self.service}"'
