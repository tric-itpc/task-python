from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import shifts_filter, time_filter
from .models import Services, TimeStamps
from .permissions import IsAdminOrStaff
from .serializer import ServiceInfoSerializer, ServiceSlaSerializer
from .serializer import StatusSaveSerializer, TimeStampsSerializer


class TimeStampsViewSet(ModelViewSet):

    serializer_class = TimeStampsSerializer
    queryset = TimeStamps.objects.all()
    pagination_class = None
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    cust_filters = [time_filter, shifts_filter]

    def get_queryset(self):
        filter_kwargs = {'name': self.kwargs['pk']}
        service = get_object_or_404(Services.objects.all(), **filter_kwargs)
        queryset = service.timestamps
        for filter in self.cust_filters:
            queryset = filter(queryset, self.request)
        return queryset

    def get_serializer_class(self):
        if '/sla' in self.request.path:
            return ServiceSlaSerializer
        return super().get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ServicesInfoViewSet(ModelViewSet):

    serializer_class = ServiceInfoSerializer
    queryset = Services.objects.all()
    pagination_class = None
    permission_classes = [IsAuthenticated, IsAdminOrStaff]


class StatusSaveViewSet(ModelViewSet):

    serializer_class = StatusSaveSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        kwargs['many'] = True
        return serializer_class(*args, **kwargs)
