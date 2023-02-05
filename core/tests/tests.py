import os

import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory

from core.tests.conftest import admin_client

from django.urls import reverse
from core.models import Service
from core.serializers import ServiceSerializer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "local_settings.py")


@pytest.mark.django_db
def test_list_services(admin_client):
    url = reverse('service-list')
    response = admin_client.get(url)

    services = Service.objects.all()
    expected_data = ServiceSerializer(services, many=True).data

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_post_service(admin_client):
    request = admin_client.post('/api/', {'name': 'Service 1', 'state': '2', 'description': '123'}, format='json')

    # service = Service.objects.create(name='Service 1', state='2', description='123')
    # expected_data = ServiceSerializer(service, many=False).data
    assert request.status_code == status.HTTP_201_CREATED
    assert Service.objects.count() == 1
    assert Service.objects.all()[0].name == 'Service 1'
