from app import db
from hashlib import sha256

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(256))
    hashed_password = db.Column(db.String(64))

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def make_user(email, password):
    query = db.select(db.func.count()).select_from(User).filter_by(email = email)
    duplicates = db.session.execute(query).scalar()
    if duplicates != 0:
        raise Exception(f"User with email {email} already registered")
    user = User(email = email, hashed_password = hash_password(password))
    db.session.add(user)
    db.session.commit()
    return user

def get_user(email):
    query = db.select(User).filter_by(email = email)
    user = db.session.execute(query).scalar()
    if user == None:
        raise Exception(f"User with email {email} does not exist")
    return user

def authenticate_user(email, password):
    user = get_user(email)
    if user.hashed_password != hash_password(password):
        raise Exception(f"User with email {email} could not be authenticated")
    return user
