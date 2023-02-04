from rest_framework import serializers

from services.models import Service, Status, Log


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        model = Service


class StatusSerializer(serializers.ModelSerializer):
    service = serializers.SlugRelatedField(slug_field='name',
                                           many=False,
                                           queryset=Service.objects.all())

    class Meta:
        fields = ('service', 'condition', 'description', 'timestamp')
        model = Status

    def validate(self, data):
        service = data.get('service')
        condition = data.get('condition')
        request_method = self.context.get('request').method
        if request_method == 'POST':
            if Status.objects.filter(
                    service=service,
                    condition=condition).exists():
                raise serializers.ValidationError(
                    f'Сервис {service.name} уже в состоянии {condition}')
        return data

class LogSerializer(serializers.ModelSerializer):
    service = serializers.SlugRelatedField(slug_field='name',
                                               queryset=Service.objects.all())

    class Meta:
        fields = ('id', 'service', 'condition', 'timestamp')
        model = Log


class SLASerializer(serializers.Serializer):
    name = serializers.CharField()
    down_time = serializers.DateTimeField()
    SLA = serializers.CharField()
