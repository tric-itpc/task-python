from django.contrib import admin

from .models import Services, TimeStamps


class ServicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


class TimeStampsAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'time_stamp',
                    'status', 'description')
    search_fields = ('service', 'status')
    list_filter = ('service', 'status')
    empty_value_display = '-пусто-'


admin.site.register(Services, ServicesAdmin)
admin.site.register(TimeStamps, TimeStampsAdmin)
