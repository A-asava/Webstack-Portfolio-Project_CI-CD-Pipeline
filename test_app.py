import pytest
from app import app, db
from models import User, Job
from flask_bcrypt import generate_password_hash

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Adding a test user
            hashed_password = generate_password_hash("password").decode('utf-8')
            user = User(username="testuser", email="testuser@example.com", password=hashed_password)
            db.session.add(user)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_register(client):
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password',
        'confirm_password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Your account has been created! You are now able to log in' in response.data

def test_login(client):
    response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_logout(client):
    client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

def test_apply_job(client):
    # First add a job to apply to
    with app.app_context():
        job = Job(title='Software Engineer', description='Test job description')
        db.session.add(job)
        db.session.commit()

    # Login first
    client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password'
    }, follow_redirects=True)

    # Apply to the job
    response = client.post('/apply/1', data={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'phone': '1234567890',
        'highest_education': 'Bachelors',
        'institution': 'Test University',
        'company_name': 'Test Company',
        'job_title_experience': 'Developer',
        'start_date': '2020-01-01',
        'end_date': '2021-01-01',
        'cover_letter': 'I am interested in this job.'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Your application has been submitted!' in response.data

def test_forgot_password(client):
    response = client.post('/forgot_password', data={
        'email': 'testuser@example.com'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'A password reset link has been sent to your email address.' in response.data


