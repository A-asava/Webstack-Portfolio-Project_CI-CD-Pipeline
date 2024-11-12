# test.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello, welcome to said's CI/CD demo app!" in response.data

def test_tasks(client):
    """Test the tasks page."""
    response = client.get('/tasks')
    assert response.status_code == 200
    assert b"This is where the tasks will be displayed." in response.data


