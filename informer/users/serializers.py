from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password', 'id')
        extra_kwargs = {'email': {'required': True},
                        'first_name': {'required': True},
                        'last_name': {'required': True}, }

    def validate(self, attrs):
        email = attrs.get('email')
        if self.Meta.model.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': f'user with email {email} is already created'}
            )
        return super().validate(attrs)
