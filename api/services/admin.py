from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Service, ServiceStatus, Status

EVD = '-пусто-'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
    )
    empty_value_display = EVD


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
    )
    empty_value_display = EVD


@admin.register(ServiceStatus)
class ServiceStatusAdmin(admin.ModelAdmin):

    list_display = ('pk', 'service', 'status', 'date_time', 'description')
    empty_value_display = EVD
