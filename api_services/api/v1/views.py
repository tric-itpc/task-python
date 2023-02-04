import datetime

from django.utils.timezone import utc
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .serializers import StatusSerializer, ServiceSerializer, LogSerializer
from services.models import Status, Service, Log
from .permissions import IsAdminOrReadOnly
from .filters import LogFilter


class LogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    filterset_class = LogFilter
    filterset_fields = ('service',)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (IsAdminOrReadOnly,)


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.order_by('-timestamp')
    serializer_class = StatusSerializer


@api_view(['GET'])
def SLAView(request, service_name):
    service = get_object_or_404(Service, name=service_name)
    service_logs = Log.objects.filter(service=service)
    if not service_logs:
        return Response(
            'Сервис пока что не имеет истории изменения статусов.',
            status=status.HTTP_400_BAD_REQUEST
        )
    current_status = Status.objects.get(service=service)
    default_start = service_logs[0].timestamp
    default_end = datetime.datetime.now().replace(tzinfo=utc)
    start = request.query_params.get('start')
    end = request.query_params.get('end')
    if not start:
        start = default_start
    else:
        start = datetime.datetime.strptime(
            start, '%Y-%m-%d %H:%M:%S').replace(tzinfo=utc)
        if start < default_start:
            start = default_start
    if not end:
        end = default_end
    else:
        end = datetime.datetime.strptime(
            end, '%Y-%m-%d %H:%M:%S').replace(tzinfo=utc)
    now = datetime.datetime.now().replace(tzinfo=utc)
    if start > now or end > now:
        return Response(
            'Проверьте промежуток времени.',
            status=status.HTTP_400_BAD_REQUEST
        )
    down_time = datetime.timedelta()
    for i in range(len(service_logs) - 1):
        log = service_logs[i]
        last_log = service_logs.last()
        if log.is_down and service_logs[i+1].timestamp > start and log.timestamp < end:
            down_time += service_logs[i+1].timestamp - log.timestamp
        if last_log.is_down and last_log.timestamp < end and i != len(service_logs) - 1:
            down_time += end - last_log.timestamp
    if current_status.condition == 'down' and current_status.timestamp < end:
        if current_status.timestamp < start:
            down_time += end - start
        else:
            down_time += end - current_status.timestamp
    SLA = (end - start - down_time) / (end - start) * 100
    data = {
        'name': service_name,
        'down_time': str(datetime.timedelta(seconds=down_time.total_seconds())),
        'SLA': f'{SLA:.3f} %'
    }
    return Response(data=data, status=status.HTTP_200_OK)
