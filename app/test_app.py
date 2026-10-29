import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endppoint(client):
    response = client.get('/health')

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_root_endpoint(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b"Welcome" in response.data
