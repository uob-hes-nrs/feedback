from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Initialize Flask app
app = Flask(__name__)

# Set a secret key for session management
app.secret_key = 'your_secret_key_here'  # Set your own unique secret key

# Initialize Firebase Admin SDK
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
    
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    id_token = request.headers.get('Authorization')
    uid, role = authenticate_user(id_token)
    if uid:
        return jsonify({"message": "Authenticated", "uid": uid, "role": role})
    return jsonify({"error": "Unauthorized"}), 403


# Views for different user roles
@app.route('/moduleorganizer_view')
def module_organiser_view():
    if 'uid' not in session or session['role'] != 'moduleorganizer':
        return redirect(url_for('index'))
    return render_template('moduleorganizer_view.html')

@app.route('/marker_view')
def marker_view():
    if 'uid' not in session or session['role'] != 'marker':
        return redirect(url_for('index'))
    return render_template('marker_view.html')

@app.route('/student_view')
def student_view():
    if 'uid' not in session or session['role'] != 'student':
        return redirect(url_for('index'))
    return render_template('student_view.html')

@app.route('/')
def home():
    return {"message": "Welcome to the prototype backend!"}

if __name__ == '__main__':
    app.run(debug=True, port=8080)