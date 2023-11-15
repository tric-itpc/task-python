import uuid

from django.core.validators import URLValidator
from django.db import models

SERVICE_STATE_CHOICES = (
    ("Работает", "working"),
    ("Не работает", "not working"),
    ("Работает нестабильно", "works unstable"),
    ("Нет данных", "no data"),
)


class Service(models.Model):
    key = models.CharField(max_length=50, unique=True)
    name = models.CharField(
        max_length=30, verbose_name="Название", blank=False, unique=True
    )
    url = models.URLField(
        verbose_name="Ссылка", null=True, blank=True, validators=[URLValidator]
    )
    description = models.CharField(
        max_length=100, verbose_name="Описание", null=True, blank=True
    )
    is_active = models.BooleanField(default=True, verbose_name="Активность")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="дата создания сервиса"
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = str(uuid.uuid4())
        return super().save(*args, **kwargs)


class ServiceState(models.Model):
    service = models.ForeignKey(
        Service,
        related_name="service_state",
        on_delete=models.CASCADE,
        verbose_name="Сервис",
    )
    state = models.CharField(
        verbose_name="Статус сервиса",
        choices=SERVICE_STATE_CHOICES,
        max_length=20,
        default="Нет данных",
    )
    description = models.CharField(
        max_length=100, verbose_name="Описание", null=True, blank=True
    )
    datetime = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания записи состояния"
    )
    relevance = models.BooleanField(default=True, verbose_name="Актуальность")
