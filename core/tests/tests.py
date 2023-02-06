import pytest
from rest_framework import status

from core.models import Service


@pytest.mark.django_db
def test_list_services(admin_client, load_test_services, services_list_url):
    response = admin_client.get(services_list_url)

    expected_data = [
        {
            "url": "http://testserver/api/details/demo-service",
            "name": "Demo Service",
            "slug_name": "demo-service",
            "state": 1,
            "description": "demo service",
            "created_at": "2023-02-04 22:28:53",
            "sla": "99.952%",
            "total_downtime": "41.135s"
        },
        {
            "url": "http://testserver/api/details/demo-service1",
            "name": "Demo Service1",
            "slug_name": "demo-service1",
            "state": 1,
            "description": "Demo Service1 working",
            "created_at": "2023-02-05 17:01:24",
            "sla": "95.973%",
            "total_downtime": "3471.67s"
        }
    ]

    assert response.status_code == status.HTTP_200_OK, response.data
    assert len(response.data) == len(expected_data), 'Length of returned services do not match'

    for response_obj, expected_obj in zip(response.data, expected_data):
        assert response_obj == expected_obj


@pytest.mark.django_db
def test_post_service(admin_client, services_list_url):
    expected_data = {'name': 'Service 1', 'state': 2, 'description': '123'}

    response = admin_client.post(services_list_url, expected_data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Service.objects.count() == 1

    obj = Service.objects.first()
    actual_data = {key: getattr(obj, key)
                   for key in expected_data}

    assert actual_data == expected_data
