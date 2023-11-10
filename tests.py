from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_service_create_correct():

   response = client.post('/service/', json={"name": "Сервис1", "state":
      "работает", "description": "string"})
   assert response.status_code == 200 or response.status_code == 400


def test_update_service():
   response = client.put('/service/Сервис1', json={"name": "Сервис1", "state":
      "не работает", "description": "string"})
   assert response.status_code == 200


def test_get_service_history():
   response = client.get('service/history/Сервис1')
   assert response.status_code == 200

def test_get_service():
   response = client.get('/service/get_services/')
   assert response.status_code == 200

def test_get_services_by_state():
   response = client.get('/service/работает/')
   assert response.status_code == 200

def test_sla_calc():
   client.put('/service/Сервис1', json={"name": "Сервис1", "state":
      "работает", "description": "string"})
   response = client.get('/service/sla/Сервис1/?name=Сервис1&start=2023-11-7&end=2023-11-9')

   assert response.status_code == 200
