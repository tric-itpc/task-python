from rest_framework import generics, mixins, viewsets
from django.shortcuts import get_object_or_404


from .models import Service, Status, ServiceStatus
from api.serializers import (
    ServiceStatusSerializer,
    ServiceSerializer,
    ServiceStatusCreateSerializer,
)


class CreateListViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    pass


class ServiceStatusList(generics.ListAPIView):
    """View-класс для отображения истории состояния конкретного сервиса"""

    queryset = ServiceStatus.objects.all()
    serializer_class = ServiceStatusSerializer

    def get_queryset(self):
        service = get_object_or_404(
            Service, name=self.kwargs.get('service_name')
        )
        return ServiceStatus.objects.filter(service=service.id)


class ServiceListCreate(CreateListViewSet):
    """View-класс для записи состояния сервиса
    и отображения списка сервисов с их текущими состояниями"""

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceSerializer
        return ServiceStatusCreateSerializer
