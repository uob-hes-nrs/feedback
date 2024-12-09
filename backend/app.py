from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///csrs.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

from auth import auth

app.register_blueprint(auth)

@app.get("/")
def root():
    return redirect("/login")

with app.app_context():
    db.create_all()
