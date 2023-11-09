from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_service_create_correct():
   response = client.post('/service/', json={"name": "Сервис4", "state": "работает", "description": "string"})
   print(response.status_code)

def test_service_create_incorrect():
   response = client.post('/service/', json={"name": "Сервис1", "state": "работает", "description": "string"})
   print(response.status_code)

def test_get_services_by_state():
   response = client.get('http://127.0.0.1:8080/service/работает/')
   print(response)

def test_sla_calc():
   response = client.get('/service/sla/Сервис1/?name=Сервис1&start=2023-11-7&end=2023-11-9')
   print(response)
