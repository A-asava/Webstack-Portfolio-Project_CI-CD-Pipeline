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
    assert b"Hello, welcome to Saidi's CI/CD demo app!" in response.data

def test_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert b"Tasks" in response.data

def test_security_headers(client):
    """Test that security headers are present in the response."""
    response = client.get('/')
    assert 'X-Content-Type-Options' in response.headers
    assert response.headers['X-Content-Type-Options'] == 'nosniff'
    assert 'X-Frame-Options' in response.headers
    assert response.headers['X-Frame-Options'] == 'DENY'

