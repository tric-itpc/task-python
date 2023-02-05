import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from core.models import Service

test_user_credentials = {
    'username': 'ernest',
    'password': '123'
}


@pytest.fixture
def admin_client() -> APIClient:
    User.objects.create_user(**test_user_credentials, pk=0,
                             # Set pk to zero so that admin user is not overridden by test data
                             is_superuser=True, is_staff=True)
    client = APIClient()
    client.login(**test_user_credentials)
    return client


@pytest.fixture
def service_records():
    Service.objects.bulk_create([
        Service(name='Service 1', state='2', description='123'),
        Service(name='', state='', description=''),
        Service(name='', state='', description=''),
        Service(name='', state='', description=''),
        Service(name='', state='', description=''),
        Service(name='', state='', description=''),
        Service(name='', state='', description=''),
        Service(name='', state='', description=''),
        Service(name='', state='', description=''),
        Service(name='', state='', description=''),
        Service(name='', state='', description=''),
    ])
