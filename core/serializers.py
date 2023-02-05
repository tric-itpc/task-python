import re
from datetime import datetime

from rest_framework import serializers

from .models import Service


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    serializer_related_field = serializers.HyperlinkedRelatedField
    serializer_related_field.lookup_field = 'slug_name'
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", default=datetime.now)

    sla = serializers.SerializerMethodField()
    total_downtime = serializers.SerializerMethodField()

    @staticmethod
    def get_total_downtime(obj) -> float or None:
        """
        Returns the total time that the service has been down.
        """

        services = Service.objects.filter(slug_name=obj.slug_name).order_by('created_at')
        downtime = 0

        if len(services) == 0:
            return

        current_not_working = None
        for i, service in enumerate(services):
            if current_not_working is None and service.state == Service.StateType.NOT_WORKING:
                current_not_working = service
            elif current_not_working is not None and service.state != Service.StateType.NOT_WORKING:
                downtime += service.created_at.timestamp() - current_not_working.created_at.timestamp()
                current_not_working = None

        if current_not_working is not None:
            downtime += datetime.now().timestamp() - current_not_working.created_at.replace(tzinfo=None).timestamp()
        return f'{str(round(downtime, 3))}s'

    def get_sla(self, obj) -> str:
        """
        Returns Service's SLA as a percentage to the 3rd decimal point.
        """

        downtime = float(re.findall(r"[-+]?\d*\.\d+|\d+", self.get_total_downtime(obj))[0])
        sla = round(100 - downtime * 0.00116, 3)
        if sla == 0:
            return '0%'
        return f'{sla}%'

    class Meta:
        model = Service
        fields = ['url', 'name', 'slug_name', 'state', 'description', 'created_at', 'sla', 'total_downtime']
        read_only_fields = ['slug_name', 'created_at']
