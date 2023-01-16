from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from djoser.views import UserViewSet
from rest_framework import pagination, permissions

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = UserSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'

    def get_queryset(self):
        return User.objects.all()
