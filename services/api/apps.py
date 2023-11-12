from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from django.db.models.signals import post_save, pre_save
        from django.dispatch import receiver
        from django.utils import timezone

        from .models import Service, StatusHistory

        @receiver(post_save, sender=Service)
        def model_service_changed(sender, instance, **kwargs):
            """
            При изменении статуса работы сервиса будет создаваться новый
            объект StatusHistory.
            """

            related_instance = StatusHistory.objects.create(service=instance)
            related_instance.status = related_instance.service.status
            related_instance.save()

        @receiver(pre_save, sender=StatusHistory)
        def update_start_end_time(sender, instance, **kwargs):
            """
            Установка start_time и end_time в соответствии с
            изменениями статуса сервиса.
            """

            if instance.status == 'не работает' and not instance.start_time:
                instance.start_time = timezone.now()

            elif (instance.status == 'работает' or
                  instance.status == 'нестабильно'):
                last_down_status = StatusHistory.objects.filter(
                    status='не работает', service=instance.service_id).first()
                if last_down_status and not last_down_status.end_time:
                    last_down_status.end_time = timezone.now()
                    last_down_status.save()
