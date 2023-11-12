from rest_framework import serializers

from .models import Service, StatusHistory


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ('id', 'name', 'status', 'description')


class StatusHistorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='service.name')
    service_id = serializers.CharField(source='service.id')

    class Meta:
        model = StatusHistory
        fields = ('id', 'name', 'service_id', 'status', 'last_modified')
