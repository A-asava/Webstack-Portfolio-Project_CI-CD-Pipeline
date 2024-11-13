import sys
import os
import pytest
from bs4 import BeautifulSoup
from app import app, JOBS

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that the home page loads and shows jobs."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Kratos Careers' in response.data
    assert b'Software Engineer' in response.data
    assert b'Apply' in response.data
    assert b'disabled' in response.data

def test_api_job_endpoint_valid(client):
    """Test the API endpoint for a valid job ID."""
    response = client.get('/api/jobs/1')
    assert response.status_code == 200
    assert b'Software Engineer' in response.data

def test_api_job_endpoint_invalid(client):
    """Test the API endpoint for an invalid job ID."""
    response = client.get('/api/jobs/999')
    assert response.status_code == 404
    assert b'Job not found' in response.data

def test_static_assets(client):
    """Test that static assets are accessible."""
    response = client.get('/static/logo.jpg')
    assert response.status_code == 200

def test_nonexistent_route(client):
    """Test that a non-existent route returns a 404 error."""
    response = client.get('/nonexistent')
    assert response.status_code == 404

def test_modal_button(client):
    """Test that the job details button is present on job cards."""
    response = client.get('/')
    assert b'View Details' in response.data

def test_correct_number_of_jobs(client):
    """Test that the correct number of jobs is listed on the homepage."""
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    job_cards = soup.find_all(class_='job-card')
    assert len(job_cards) == len(JOBS)

