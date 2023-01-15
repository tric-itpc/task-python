from datetime import timedelta
from rest_framework import serializers

from .models import Services, TimeStamps


class TimeStampsSerializer(serializers.ModelSerializer):
    service = serializers.SlugRelatedField(
        queryset=Services.objects.all(),
        slug_field='name')

    class Meta:
        model = TimeStamps
        fields = ['service', 'time_stamp', 'status', 'description']


class ServiceSlaSerializer(serializers.Serializer):
    sla = serializers.SerializerMethodField()

    def get_sla(self, obj):
        queryset = self.instance
        amount = len(queryset)
        if amount <= 1:
            return 0
        full_time = queryset.last().time_stamp - queryset.first().time_stamp
        work_time = timedelta()
        start = None
        time_stamp = None
        for num, elem in enumerate(queryset):
            if start is None:
                if elem.status == 'working':
                    start = elem.time_stamp
            else:
                prev_status = queryset[num - 1].status
                if elem.status != 'working' and prev_status == 'working':
                    time_stamp = queryset[num - 1].time_stamp
                elif elem.status == 'working' and (
                        prev_status == 'working' and num == amount - 1):
                    time_stamp = elem.time_stamp
                if time_stamp:
                    work_time += time_stamp - start
                    start = None
                    time_stamp = None

        if work_time == 0:
            return 0

        return round(work_time/full_time, 3)


class ServiceInfoSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    time_stamp = serializers.SerializerMethodField()
    service_descr = serializers.CharField(source='description')

    class Meta:
        model = Services
        fields = ['id', 'name', 'status', 'time_stamp', 'service_descr']

    def get_status(self, obj):

        last_record = self._context.get('last_record')
        # для уменьшения количества обращений к БД
        if not last_record:
            last_record = obj.timestamps.last()
            self._context['last_record'] = last_record
        else:
            self._context['last_record'] = None

        return last_record.status

    def get_time_stamp(self, obj):
        last_record = self._context.get('last_record')
        # для уменьшения количества обращений к БД
        if not last_record:
            last_record = obj.timestamps.last()
            self._context['last_record'] = last_record
        else:
            self._context['last_record'] = None
        return last_record.time_stamp


class StatusSaveSerializer(serializers.ModelSerializer):
    service = serializers.SlugRelatedField(
        queryset=Services.objects.all(),
        slug_field='name')

    class Meta:
        model = TimeStamps
        fields = ['service', 'status', 'description']
