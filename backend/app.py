from flask import Flask, redirect
from auth import auth

app = Flask(__name__)

app.register_blueprint(auth)

@app.get("/")
def root():
    return redirect("/login")
