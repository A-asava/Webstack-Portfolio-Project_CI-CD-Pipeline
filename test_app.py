import pytest
from app import app

@pytest.fixture
def client():
    # Set up a test client for the Flask application
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello, welcome to said's CI/CD demo app!" in response.data

def test_tasks(client):
    """Test the tasks route"""
    response = client.get('/tasks')
    assert response.status_code == 200
    assert b"This is where the tasks will be displayed." in response.data

def test_home_method_not_allowed(client):
    """Test an unsupported method on the home route"""
    response = client.post('/')
    assert response.status_code == 405  # Method Not Allowed

def test_tasks_method_not_allowed(client):
    """Test an unsupported method on the tasks route"""
    response = client.post('/tasks')
    assert response.status_code == 405  # Method Not Allowed

def test_404_not_found(client):
    """Test a route that does not exist"""
    response = client.get('/nonexistent')
    assert response.status_code == 404

