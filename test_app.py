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

def test_get_tasks_empty(client):
    """Test retrieving tasks when none are present"""
    response = client.get('/tasks')
    assert response.status_code == 200
    assert response.json == {"tasks": []}

def test_add_task(client):
    """Test adding a new task"""
    response = client.post('/tasks', json={"task": "Test Task"})
    assert response.status_code == 201
    assert response.json["message"] == "Task added successfully."

def test_get_tasks_with_data(client):
    """Test retrieving tasks when some are present"""
    client.post('/tasks', json={"task": "Test Task"})
    response = client.get('/tasks')
    assert response.status_code == 200
    assert "tasks" in response.json
    assert "Test Task" in response.json["tasks"]

def test_add_task_no_data(client):
    """Test adding a task without providing data"""
    response = client.post('/tasks', json={})
    assert response.status_code == 400
    assert response.json["error"] == "No task provided."

def test_get_task(client):
    """Test retrieving a specific task"""
    client.post('/tasks', json={"task": "Test Task"})
    response = client.get('/tasks/0')
    assert response.status_code == 200
    assert response.json["task"] == "Test Task"

def test_get_task_not_found(client):
    """Test retrieving a task that does not exist"""
    response = client.get('/tasks/99')
    assert response.status_code == 404
    assert response.json["error"] == "Task not found."

def test_home_method_not_allowed(client):
    """Test an unsupported method on the home route"""
    response = client.post('/')
    assert response.status_code == 405  # Method Not Allowed

def test_tasks_method_not_allowed(client):
    """Test an unsupported method on the tasks route"""
    response = client.put('/tasks')
    assert response.status_code == 405  # Method Not Allowed

