from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User
from app import db
from app.api.errors import error_response
from flask import g


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        if not username or not password:
            return False
        new_user = User(username=username)
        new_user.set_password(password=password)
        db.session.add(new_user)
        db.session.commit()
        g.current_user = new_user
        return True
    g.current_user = user
    return user.check_password(password)

@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)

@token_auth.verify_token
def verify_token(token):
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None
    
@token_auth.error_handler
def token_auth_error():
    return error_response(401)