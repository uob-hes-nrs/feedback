from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Assignment, AssessmentFormat

module_routes = Blueprint('module_routes', __name__)

@module_routes.route('/create_assignment', methods=['GET', 'POST'])
def create_assignment():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        total_marks = request.form['total_marks']
        assignment = Assignment(title=title, description=description, total_marks=total_marks)
        db.session.add(assignment)
        db.session.commit()
        return redirect(url_for('module_routes.view_assignments'))
    return render_template('create_format.html')

@module_routes.route('/view_assignments')
def view_assignments():
    assignments = Assignment.query.all()
    return render_template('assignments.html', assignments=assignments)
