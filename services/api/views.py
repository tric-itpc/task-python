from datetime import datetime, timedelta

from rest_framework import decorators, mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Service, StatusHistory
from .scripts import seconds_to_time
from .serializers import ServiceSerializer, StatusHistorySerializer


class ServiceViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    """Вьюсет для создания и получения информации о сервисах."""

    permission_classes = [AllowAny]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def perform_create(self, serializer):
        serializer.save()


class StatusHistoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Вьюсет для получения истории изменений состояния по id сервиса."""

    serializer_class = StatusHistorySerializer

    def get_queryset(self):
        service_id = self.kwargs.get('service_id')
        return StatusHistory.objects.filter(service__id=service_id)


@decorators.api_view(['GET'])
def sla_calculation(request, service_id, start_date, end_date):
    """
    Вьюсет для подсчета общего времени недоступности сервиса и расчёта
    SLA за заданный интервал времени.
    """

    service_downtime = StatusHistory.objects.filter(
        service_id=service_id,
        status='не работает',
        last_modified__range=[start_date, end_date]
    )

    total_downtime = timedelta()
    for downtime in service_downtime:
        total_downtime += downtime.downtime_duration

    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    total_time = end_date - start_date
    availability = (total_time - total_downtime) / total_time
    sla = availability * 100
    total = seconds_to_time(total_downtime.seconds)

    return Response(
        {
            'Информация для сервиса': Service.objects.get(id=service_id).name,
            'Service level agreement(в процентах)': round(sla, 3),
            'Общее время недоступности сервиса': total
         },
        status=status.HTTP_200_OK
    )
