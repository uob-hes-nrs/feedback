from backend.app1 import db

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    total_marks = db.Column(db.Integer, nullable=False)

class AssessmentFormat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    component_title = db.Column(db.String(120), nullable=False)
    component_marks = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    total_marks = db.Column(db.Integer, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
