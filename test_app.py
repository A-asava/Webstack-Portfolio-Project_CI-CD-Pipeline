import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home route for a successful response and correct content."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello, welcome to Saidi's CI/CD demo app!" in response.data

def test_tasks(client):
    """Test the tasks route for a successful response and correct content."""
    response = client.get('/tasks')
    assert response.status_code == 200
    assert b"This is where the tasks will be displayed." in response.data

def test_about(client):
    """Test the about page."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b"This page provides information about the application." in response.data

def test_nonexistent_route(client):
    """Test a route that does not exist to ensure proper error handling."""
    response = client.get('/nonexistent')
    assert response.status_code == 404

def test_security_headers(client):
    """Test security-related headers for best practices."""
    response = client.get('/')
    assert 'X-Content-Type-Options' in response.headers
    assert response.headers['X-Content-Type-Options'] == 'nosniff'
    assert 'X-Frame-Options' in response.headers
    assert response.headers['X-Frame-Options'] == 'DENY'

def test_invalid_method(client):
    """Test that an invalid method returns a 405 Method Not Allowed."""
    response = client.post('/')
    assert response.status_code == 405

