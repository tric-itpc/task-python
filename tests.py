from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_service_create_correct():
   response = client.post('/service/', json={"name": "Сервис1", "state": "работает"})
   print(response.status_code)

def test_service_create_incorrect():
   response = client.post('/service/', json={"name": "Сервис1", "state": "работает"})
   print(response.status_code)
