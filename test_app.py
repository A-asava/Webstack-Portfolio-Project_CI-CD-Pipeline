import pytest
from app import app  # Ensure the app module is correctly imported

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Saidi's CI/CD demo app!" in response.data

def test_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert b"Task Page" in response.data  # Check for expected content

def test_about(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b"This app demonstrates a simple CI/CD pipeline." in response.data

def test_404(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404  # Check for 404 response on unknown route

def test_security_headers(client):
    response = client.get('/')
    assert 'X-Content-Type-Options' in response.headers
    assert response.headers['X-Content-Type-Options'] == 'nosniff'
    assert 'X-Frame-Options' in response.headers
    assert response.headers['X-Frame-Options'] == 'DENY'

