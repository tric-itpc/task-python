from django.contrib import admin

from .models import Service, StatusHistory


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'description')
    search_fields = ('name', 'description')
    list_filter = ('status',)


@admin.register(StatusHistory)
class StatusHistorysAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'status', 'date')
    search_fields = ('service__name',)
    list_filter = ('status',)

    def date(self, obj):
        return obj.last_modified.strftime('%d.%m.%Y %H:%M:%S')
    date.short_description = 'Дата изменения'
