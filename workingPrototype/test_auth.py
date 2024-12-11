from flask import Flask, session
from unittest.mock import patch, Mock
from auth_user import authenticate_user  # Import the function to test

# Set up a Flask app for testing the session
app = Flask(__name__)
app.secret_key = "test_secret_key"  # Flask secret key for session handling

def test_authenticate_user():
    with app.test_request_context():
        # Mock Firebase auth and Firestore
        mock_auth = Mock()
        mock_db = Mock()

        # Mocked token and user data
        mock_id_token = "mock_id_token"
        mock_decoded_token = {"uid": "test_uid"}
        mock_user_data = {"role": "admin"}

        # Mock Firestore document
        mock_user_doc = Mock()
        mock_user_doc.exists = True
        mock_user_doc.to_dict.return_value = mock_user_data

        # Patch the Firebase methods
        with patch("auth_user.auth", mock_auth), patch("auth_user.db", mock_db):
            # Mock verify_id_token
            mock_auth.verify_id_token.return_value = mock_decoded_token

            # Mock Firestore document retrieval
            mock_db.collection.return_value.document.return_value.get.return_value = mock_user_doc

            # Call the function
            uid, role = authenticate_user(mock_id_token)

            # Assertions
            assert uid == "test_uid", "UID mismatch"
            assert role == "admin", "Role mismatch"
            assert session["uid"] == "test_uid", "Session UID mismatch"
            assert session["role"] == "admin", "Session role mismatch"

            # Print results for confirmation
            print(f"Test Passed: UID={uid}, Role={role}")
            print(f"Session: {session}")

if __name__ == "__main__":
    test_authenticate_user()
