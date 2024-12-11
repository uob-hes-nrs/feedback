import pytest
from unittest.mock import patch, Mock
from app import app  # Import the Flask app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.secret_key = 'test_secret_key'
    with app.test_client() as client:
        yield client

# Mock Firebase initialization globally
@pytest.fixture(autouse=True)
def mock_firebase():
    with patch("firebase_admin.initialize_app"), patch("firebase_admin.firestore.client") as mock_firestore_client:
        yield mock_firestore_client

# Test the index route
def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"<title>" in response.data  # Check for presence of HTML content

# Test login route with valid token
def test_login_success(client, mock_firebase):
    mock_auth = Mock()
    mock_db = mock_firebase.return_value

    # Mock Firebase token verification and user role retrieval
    mock_id_token = "valid_id_token"
    mock_decoded_token = {"uid": "test_uid"}
    mock_user_data = {"role": "moduleorganizer"}

    # Mock Firestore document
    mock_user_doc = Mock()
    mock_user_doc.exists = True
    mock_user_doc.to_dict.return_value = mock_user_data

    with patch("app.auth", mock_auth):
        mock_auth.verify_id_token.return_value = mock_decoded_token
        mock_db.collection.return_value.document.return_value.get.return_value = mock_user_doc

        response = client.post('/login', headers={"Authorization": f"Bearer {mock_id_token}"})
        data = response.get_json()

        assert response.status_code == 200
        assert data["message"] == "Authenticated"
        assert data["uid"] == "test_uid"
        assert data["role"] == "moduleorganizer"

# Test unauthorized access to a protected route
def test_protected_route_unauthorized(client):
    response = client.post('/create_assignment', json={
        "title": "Test Assignment",
        "description": "Test Description",
        "deadline": "2024-12-31",
        "feedback_form_id": "test_feedback_form_id"
    })
    assert response.status_code == 403
    assert response.get_json()["error"] == "Unauthorized"

# Test moduleorganizer creating an assignment
def test_create_assignment(client, mock_firebase):
    with client.session_transaction() as sess:
        sess['uid'] = 'test_uid'
        sess['role'] = 'moduleorganizer'

    mock_db = mock_firebase.return_value
    assignment_ref = Mock()
    assignment_ref.id = "test_assignment_id"
    mock_db.collection.return_value.document.return_value = assignment_ref

    response = client.post('/create_assignment', json={
        "title": "Test Assignment",
        "description": "Test Description",
        "deadline": "2024-12-31",
        "feedback_form_id": "test_feedback_form_id"
    })

    assert response.status_code == 200
    assert response.get_json()["message"] == "Assignment created successfully"
    assert response.get_json()["assignment_id"] == "test_assignment_id"

# Test student viewing feedback
def test_view_feedback(client, mock_firebase):
    with client.session_transaction() as sess:
        sess['uid'] = 'student_uid'
        sess['role'] = 'student'

    mock_db = mock_firebase.return_value
    mock_submission_doc = Mock()
    mock_submission_doc.exists = True
    mock_submission_doc.to_dict.return_value = {
        "grades": [90, 85],
        "feedback": "Great work!"
    }

    mock_db.collection.return_value.document.return_value.get.return_value = mock_submission_doc

    response = client.get('/view_feedback/test_submission_id')

    assert response.status_code == 200
    data = response.get_json()
    assert data["grades"] == [90, 85]
    assert data["feedback"] == "Great work!"