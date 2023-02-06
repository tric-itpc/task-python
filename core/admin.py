from django.contrib import admin

from core.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Model to display Services in admin panel.
    """
    list_display = ('name', 'slug_name', 'state', 'created_at')

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('slug_name', '-created_at').distinct('slug_name')
