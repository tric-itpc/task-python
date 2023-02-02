from django.contrib import admin

from services.models import Service, Status, Log


@admin.register(Service)
class AdminService(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Status)
class AdminStatus(admin.ModelAdmin):
    list_display = ('pk', 'service', 'condition', 'timestamp')


@admin.register(Log)
class AdminLog(admin.ModelAdmin):
    list_display = ('pk', 'service', 'condition', 'timestamp')
