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

def test_profile(client):
    response = client.get('/profile')
    assert response.status_code == 200
    assert b"This is the user profile page." in response.data

def test_about(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b"This page provides information about the application." in response.data

def test_contact(client):
    response = client.get('/contact')
    assert response.status_code == 200
    assert b"This is the contact page." in response.data

