from app import db
from user import User, make_user, get_user, authenticate_user
from flask import Blueprint, make_response, redirect, render_template, request
from secrets import token_hex

class Session(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    token = db.Column(db.String(64))

def make_token(user):
    session = Session()
    session.user_id = user.id
    session.token = token_hex(64)
    db.session.add(session)
    db.session.commit()
    return session.token

def resolve_token(token):
    query = db.select(User).join(Session).filter_by(token = token)
    user = db.session.execute(query).scalar()
    if user == None:
        raise Exception("Invalid session token")
    return user

def delete_token(token):
    query = db.select(Session).filter_by(token = token)
    session = db.session.execute(query).scalar()
    db.session.delete(session)
    db.session.commit()

auth = Blueprint("auth", __name__)

@auth.get("/login")
def get_login():
    try:
        user = resolve_token(request.cookies.get("Authentication"))
        return redirect("/logout")
    except:
        return render_template("login.html")

@auth.post("/login")
def post_login():
    try:
        try:
            user = make_user(request.form["email"], request.form["password"])
        except:
            user = authenticate_user(request.form["email"], request.form["password"])
        token = make_token(user)
        response = redirect("/logout")
        response.set_cookie("Authentication", token, secure = True)
        return response
    except:
        return make_response("Bad credentials", 401)

@auth.get("/logout")
def get_logout():
    try:
        user = resolve_token(request.cookies.get("Authentication"))
        return render_template("logout.html")
    except:
        return redirect("/logout")

@auth.post("/logout")
def post_logout():
    try:
        token = request.cookies.get("Authentication")
        user = resolve_token(token)
        delete_token(token)
        response = redirect("/login")
        response.delete_cookie("Authentication")
        return response
    except:
        return make_response("No credentials", 401)
