from rest_framework import serializers
from services.models import Service, ServiceStatus, Status


class ServiceStatusSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения истории состояний конкретного сервиса"""

    service = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)

    def get_service(self, obj):
        return obj.service.name

    def get_status(self, obj):
        return obj.status.name

    class Meta:
        model = ServiceStatus
        fields = ('service', 'status', 'description', 'date_time')
        read_only_fields = ('date_time',)


class ServiceStatusCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для записи изменений в состоянии сервиса"""

    service = serializers.SlugRelatedField(
        slug_field='name', queryset=Service.objects.all()
    )
    status = serializers.SlugRelatedField(
        slug_field='name', queryset=Status.objects.all()
    )

    class Meta:
        model = ServiceStatus
        fields = ('service', 'status', 'description')


class ServiceSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения списка сервисов с их текущим состоянием"""

    service = serializers.ReadOnlyField(source='name')
    status = serializers.SerializerMethodField(read_only=True)

    def get_status(self, obj):
        return (
            ServiceStatus.objects.filter(service=obj)
            .latest('date_time')
            .status.name
        )

    class Meta:
        model = Service
        fields = (
            'service',
            'status',
        )
        read_only_fields = (
            'service',
            'status',
        )
