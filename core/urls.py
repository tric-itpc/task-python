from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from .views import ServiceListApiView, ServiceDetailsApiView

urlpatterns = [
    path('api/', ServiceListApiView.as_view(), name='service-list'),
    path('api/details/<str:slug_name>', ServiceDetailsApiView.as_view(), name='service-detail'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
