from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .filters import time_filter, shifts_filter
from .models import Services, TimeStamps
from .serializer import TimeStampsSerializer


class TimeStampsViewSet(ModelViewSet):

    serializer_class = TimeStampsSerializer
    queryset = TimeStamps.objects.all()
    pagination_class = None
    permission_classes = []
    cust_filters = [time_filter, shifts_filter]

    def get_queryset(self):
        filter_kwargs = {'id': self.kwargs['pk']}
        service = get_object_or_404(Services.objects.all(), **filter_kwargs)
        queryset = service.timestamps
        for filter in self.cust_filters:
            queryset = filter(queryset, self.request)
        return queryset
