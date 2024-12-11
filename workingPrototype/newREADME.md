Overview

This project implements a Flask-based system for allowing module organisers to have a little more creativity when it comes to responding to user submissions to assignments. The test script ensures the applications functionality by testing authentication and role based access. 

Features
	1.	Authentication:
	•	Verifies Firebase ID tokens and retrieves user roles.
	2.	Role-Based Access:
	•	Module Organizer: Create assignments and feedback forms.
	•	Marker: Grade submissions.
	•	Student: View feedback and submissions.
	3.	Database Operations:
	•	CRUD operations on Firestore for assignments, submissions, and feedback forms.

1) add_dummy_data.py DOES NOT need to be run

2) Run app.py to run the flask server and connect to http://127.0.0.1:8080

3) Access granted to a login page with details:
    a) (Module Organiser) Email: johndoe@example.com   password: moduleorganiser
    b) (Marker) Email: janesmith@example.com   password: marker
    c) (Student) Email: alicejohnson@example.com   password: student

4) BE CAREFUL. Modifications through use of the application may create unintended database modifications

5) The database is NOT LOCAL. Cloud-based database, any modifications on the database must be done with caution.
