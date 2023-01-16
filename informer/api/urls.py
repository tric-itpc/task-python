from django.urls import path

from .views import ServicesInfoViewSet, StatusSaveViewSet, TimeStampsViewSet

urlpatterns = [
    path('info/all', ServicesInfoViewSet.as_view({'get': 'list'}),
         name='all_services'),
    path('info/<str:pk>', TimeStampsViewSet.as_view({'get': 'list'}),
         name='timestamps'),
    path('info/<str:pk>/sla', TimeStampsViewSet.as_view({'get': 'retrieve'}),
         name='sla'),
    path('set', StatusSaveViewSet.as_view({'post': 'create'}),
         name='save_status'),
]
