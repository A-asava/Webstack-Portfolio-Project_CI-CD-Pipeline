import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CI/CD Demo App</title>
        </head>
        <body>
            <h1>Hello, welcome to Saidi's CI/CD demo app!</h1>
            <p>This is a simple demo app with a basic CI/CD pipeline.</p>
            <a href="/tasks">View Tasks</a>
        </body>
        </html>
        """

    @app.route('/tasks')
    def tasks():
        return "<h1>Tasks</h1><p>This is the tasks page.</p>"

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello, welcome to Saidi's CI/CD demo app!" in response.data

def test_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert b"Tasks" in response.data

def test_security_headers(client):
    response = client.get('/')
    assert 'X-Content-Type-Options' in response.headers
    assert response.headers['X-Content-Type-Options'] == 'nosniff'
    assert 'X-Frame-Options' in response.headers
    assert response.headers['X-Frame-Options'] == 'DENY'

