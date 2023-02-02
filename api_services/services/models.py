from django.db import models


class Service(models.Model):
    name = models.CharField(verbose_name='Название сервиса',
                            max_length=256,
                            unique=True)

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

    def __str__(self):
        return self.name


class Status(models.Model):
    CONDITION_CHOICES = [
        ('up', 'up'),
        ('down', 'down'),
        ('unstable', 'unstable')
    ]
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='statuses',
        verbose_name='Сервис')
    condition = models.CharField(verbose_name='Состояние',
                                 choices=CONDITION_CHOICES, max_length=8)
    timestamp = models.DateTimeField(verbose_name='Время обновления',
                                     auto_now_add=True)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def save(self, *args, **kwargs):
        if Status.objects.filter(service=self.service).exists():
            old_status = Status.objects.get(service=self.service)
            if self.condition == old_status.condition:
                return
            Log.objects.create(condition=old_status.condition,
                               service=old_status.service,
                               timestamp=old_status.timestamp)
            old_status.delete()
        super(Status, self).save(*args, **kwargs)


class Log(models.Model):
    CONDITION_CHOICES = [
        ('up', 'up'),
        ('down', 'down'),
        ('unstable', 'unstable')
    ]
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='old_statuses',
        verbose_name='Сервис')
    condition = models.CharField(verbose_name='Состояние',
                                 choices=CONDITION_CHOICES, max_length=8)
    timestamp = models.DateTimeField(verbose_name='Время обновления')
