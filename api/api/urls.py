from django.urls import include, path
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url

from services.views import ServiceStatusList, ServiceListCreate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('service/<slug:service_name>/', ServiceStatusList.as_view()),
#    path('service/<slug:service_name>/', ServiceStatusList.as_view()),
    path(
        'service/',
        ServiceListCreate.as_view({'get': 'list', 'post': 'create'}),
    ),
]

schema_view = get_schema_view(
   openapi.Info(
      title='API',
      default_version='v1',
      description='Документация для приложения services',
      contact=openapi.Contact(email='V.V.Cherepanov@bk.ru'),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), 
       name='schema-redoc'),
] 