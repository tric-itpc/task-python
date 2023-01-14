from rest_framework import serializers

from .models import TimeStamps


class TimeStampsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeStamps
        fields = ['service', 'time_stamp', 'status', 'description']
