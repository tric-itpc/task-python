from django_filters import FilterSet, CharFilter

from services.models import Log


class LogFilter(FilterSet):
    service = CharFilter(field_name='service__name', lookup_expr='exact')

    class Meta:
        model = Log
        fields = ('service',)
