import pytest
from unittest.mock import patch, Mock

# Mock Firebase before importing auth_user
with patch("auth_user.firebase_admin.initialize_app"), patch("auth_user.firestore.client") as mock_firestore_client:
    from app import *  # Import after mocking

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.secret_key = 'test_secret_key'
    with app.test_client() as client:
        yield client

# Test the index route
def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<title>' in response.data  # Check for common HTML content

# Test the login route with invalid token
def test_login_failure(client):
    with patch("auth_user.authenticate_user", return_value=(None, None)):
        response = client.post('/login', headers={"Authorization": "invalid_token"})
        assert response.status_code == 403
        data = response.get_json()
        assert data["error"] == "Unauthorized"