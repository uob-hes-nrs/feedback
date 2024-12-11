## App.py 
# Authentication
- Verifies Firebase ID tokens to authenticate users 
- Stores users unique ID and role in the flask session 

# Role-based views
- Module Organiser 
- Marker
-Student
-Redirects unauthorised users back to login

# Renders based on users roles 

# Test Script (test_app.py)
- Tests user authetnication with firebase 
- Validates login failure, success is defined on the webpage itself. 