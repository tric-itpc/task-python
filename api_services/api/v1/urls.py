from django.urls import path, include
from rest_framework import routers

from .views import ServiceViewSet, StatusViewSet, LogViewSet, SLAView

v1_router = routers.DefaultRouter()
v1_router.register('statuses', StatusViewSet)
v1_router.register('log', LogViewSet, basename='Log')
v1_router.register('services', ServiceViewSet)


urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include(v1_router.urls)),
    path('sla/<service_name>/', SLAView, name='sla'),
]
