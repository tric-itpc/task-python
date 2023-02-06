import json

import pytest
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from core.models import Service

test_user_credentials = {
    'username': 'ernest',
    'password': '123'
}


@pytest.fixture
def load_test_services():
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.loads(file.read())

    Service.objects.bulk_create([
        Service(**obj_data)
        for obj_data in data
    ])


@pytest.fixture
def services_list_url() -> str:
    return reverse('service-list')


@pytest.fixture
def admin_client() -> APIClient:
    User.objects.create_user(**test_user_credentials, pk=0,
                             # Set pk to zero so that admin user is not overridden by test data
                             is_superuser=True, is_staff=True)
    client = APIClient()
    client.login(**test_user_credentials)
    return client


