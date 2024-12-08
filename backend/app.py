from flask import Flask, make_response
from auth import auth

app = Flask(__name__)

app.register_blueprint(auth)

@app.route("/", methods = ["GET"])
def root():
    return "Hello!"
