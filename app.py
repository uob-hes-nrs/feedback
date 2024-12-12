from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
import json
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

app.secret_key = 'CSRStesting10052323434656'  # Set your own unique secret key
# load_dotenv()

# Initialize Firebase Admin SDK
cred = credentials.Certificate("FIREBASE_KEY.json")
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

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    id_token = request.headers.get('Authorisation')
    uid, role = authenticate_user(id_token)
    if uid:
        return jsonify({"message": "Authenticated", "uid": uid, "role": role})
    return jsonify({"error": "Unauthorised"}), 403

# Middleware to ensure user is authenticated and authorised based on their role
def role_required(role):
    if 'uid' not in session or session['role'] != role:
        return jsonify({'error': 'Unauthorised'}), 403

# Route for module organisers to create assignments
@app.route('/create_assignment', methods=['POST'])
def create_assignment():
    if 'uid' not in session or session['role'] != 'moduleorganiser':
        return jsonify({'error': 'Unauthorised'}), 403

    data = request.get_json()
    feedback_form_id = data['feedback_form_id']  # Link to the feedback form created by module organiser
    assignment_ref = db.collection('assignments').document()

    assignment_ref.set({
        'title': data['title'],
        'description': data['description'],
        'deadline': data['deadline'],
        'feedback_form_id': feedback_form_id  # Link the assignment to the feedback form
    })

    return jsonify({"message": "Assignment created successfully", "assignment_id": assignment_ref.id})

# Route to get all submissions for a specific assignment
@app.route('/get_submissions/<assignment_id>', methods=['GET'])
def get_submissions(assignment_id):
    if 'uid' not in session or session['role'] != 'marker':
        return jsonify({'error': 'Unauthorised'}), 403

    submissions_ref = db.collection('submissions').where('assignment_id', '==', assignment_id)
    submissions = submissions_ref.stream()

    result = []
    for submission in submissions:
        submission_data = submission.to_dict()
        result.append({
            'submission_id': submission.id,
            'status': submission_data.get('status')
        })

    return jsonify(result)

# Route to get feedback form for a specific assignment
@app.route('/get_feedback_form/<assignment_id>', methods=['GET'])
def get_feedback_form(assignment_id):
    if 'uid' not in session:
        return jsonify({'error': 'Unauthorised'}), 403

    assignment_ref = db.collection('assignments').document(assignment_id)
    assignment = assignment_ref.get()

    if assignment.exists:
        feedback_form_id = assignment.to_dict().get('feedback_form_id')

        # Fetch the feedback form using the feedback form ID
        feedback_form_ref = db.collection('feedback_forms').document(feedback_form_id)
        feedback_form = feedback_form_ref.get()

        if feedback_form.exists:
            return jsonify(feedback_form.to_dict())

    return jsonify({'error': 'Assignment or feedback form not found'}), 404

# Route to grade a submission (for markers)
@app.route('/grade_submission', methods=['POST'])
def grade_submission():
    if 'uid' not in session or session['role'] != 'marker':
        return jsonify({'error': 'Unauthorised'}), 403

    data = request.get_json()
    submission_id = data['submission_id']
    grades = data['grades']
    feedback = data['feedback']

    submission_ref = db.collection('submissions').document(submission_id)
    submission_ref.update({
        'grades': grades,
        'feedback': feedback,
        'status': 'graded'
    })

    return jsonify({"message": "Submission graded successfully"})

# Route to create feedback forms (for module organisers)
@app.route('/create_feedback_form', methods=['POST'])
def create_feedback_form():
    if 'uid' not in session or session['role'] != 'moduleorganiser':
        return jsonify({'error': 'Unauthorised'}), 403

    data = request.get_json()
    form_title = data['form_title']
    components = data['components']

    feedback_ref = db.collection('feedback_forms').document()
    feedback_ref.set({
        'form_title': form_title,
        'components': components
    })

    return jsonify({"message": "Feedback form created successfully", "feedback_id": feedback_ref.id})

# Route to view feedback for a submission (for students)
@app.route('/view_feedback/<submission_id>', methods=['GET'])
def view_feedback(submission_id):
    if 'uid' not in session or session['role'] != 'student':
        return jsonify({'error': 'Unauthorised'}), 403

    submission_ref = db.collection('submissions').document(submission_id)
    submission = submission_ref.get()

    if submission.exists:
        return jsonify(submission.to_dict())

    return jsonify({'error': 'Submission not found'}), 404

# Route to get all submissions for the logged-in student
@app.route('/get_student_submissions', methods=['GET'])
def get_student_submissions():
    if 'uid' not in session or session['role'] != 'student':
        return jsonify({'error': 'Unauthorised'}), 403

    submissions_ref = db.collection('submissions').where('student_id', '==', session['uid'])
    submissions = submissions_ref.stream()

    result = []
    for submission in submissions:
        submission_data = submission.to_dict()
        result.append({
            'submission_id': submission.id,
            'assignment_id': submission_data.get('assignment_id'),
            'grades': submission_data.get('grades', []),
            'feedback': submission_data.get('feedback', []),
            'status': submission_data.get('status', 'not-graded')
        })

    return jsonify(result)

# Views for different user roles
@app.route('/moduleorganiser_view')
def module_organiser_view():
    if 'uid' not in session or session['role'] != 'moduleorganiser':
        return redirect(url_for('index'))
    return render_template('moduleorganiser_view.html')

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

if __name__ == '__main__':
    app.run(debug=True, port=8080)