from flask import session
import firebase_admin
from firebase_admin import firestore, credentials, auth

cred = credentials.Certificate("uobcsrs-firebase-adminsdk-5fuvt-1ac3cf19bb.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
# Function to authenticate user and store their UID and role in the session
def authenticate_user(id_token):
    try:
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        user_doc = db.collection('users').document(uid).get()

        if user_doc.exists:
            user_data = user_doc.to_dict()
            role = user_data.get('role', 'student')  # Default to 'student' if role is not found
            # Store UID and role in session
            session['uid'] = uid
            session['role'] = role
            return uid, role
        return None, None
    except Exception as e:
        print(f"Authentication error: {e}")
        return None, None
