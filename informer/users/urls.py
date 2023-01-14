from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views as user_views

router_users = SimpleRouter()

router_users.register("users", user_views.CustomUserViewSet)

urlpatterns = [
    path('', include(router_users.urls)),
]
