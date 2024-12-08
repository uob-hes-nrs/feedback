from flask import Blueprint, make_response

auth = Blueprint("auth", __name__, url_prefix = "/auth")

@auth.route("/info", methods = ["GET"])
def root():
    return make_response("Not signed in", 401)

@auth.route("/login", methods = ["POST"])
def login():
    return make_response("Not signed in", 401)

@auth.route("/logout", methods = ["POST"])
def logout():
    return make_response("Not signed in", 401)
