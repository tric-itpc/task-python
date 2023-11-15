from rest_framework import serializers

from backend.models import Service, ServiceState


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("id", "name", "url", "description", "is_active", "created_at")
        read_only_fields = ("id",)


class ServiceStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceState
        fields = (
            "id",
            "service",
            "state",
            "description",
            "datetime",
            "relevance",
        )
        read_only_fields = ("id",)
