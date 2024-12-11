# Authenticate User Function and Test Script
## Function: `authenticate_user`
### Purpose
- Verifies a Firebase ID token to authenticate users.
- Retrieves user roles from Firestore and stores the UID and role in a Flask session.
### Returns
- `(uid, role)` if authentication succeeds.
- `(None, None)` on failure.

# Test Script: `test_authenticate_user.py`
## Overview
This script tests the `authenticate_user` function by mocking Firebase authentication and Firestore database interactions.
## Purpose
- Simulates token verification and user data retrieval using mocks.
- Ensures correct UID, role, and session updates.
### Returns
- Test Passed: UID=test_uid, Role=admin
- Session: {'uid': 'test_uid', 'role': 'admin'}
if successful 

# Backend Prototype - Iteration 1
## Function
This iteration sets up the backend using Flask. It includes a single route that returns a welcome message as JSON.
### returns "message": "Welcome to the prototype backend!"

# Test Script 'test_app.py'
- Tests if the localhost is running and responds to requests 