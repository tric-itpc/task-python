from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer


User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password', 'id')
        extra_kwargs = {'email': {'required': True},
                        'first_name': {'required': True},
                        'last_name': {'required': True}, }
