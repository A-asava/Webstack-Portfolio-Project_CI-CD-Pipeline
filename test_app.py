from app import app
import pytest

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"This is a simple demo app with a basic CI/CD pipeline." in response.data

def test_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert b"This is the tasks page. You can view and manage tasks here." in response.data

def test_security_headers(client):
    response = client.get('/')
    assert 'X-Content-Type-Options' in response.headers

