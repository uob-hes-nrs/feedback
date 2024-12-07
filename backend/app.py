from flask import Flask
from user import make_user

app = Flask(__name__)

@app.route("/")
def root():
    return "Hello!"

@app.route("/auth")
def auth():
    return f"Hello, {make_user().uid}!"
