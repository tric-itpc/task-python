from django.urls import path

from .views import TimeStampsViewSet


urlpatterns = [
    path('info/<int:pk>', TimeStampsViewSet.as_view({'get': 'list'})),
]
