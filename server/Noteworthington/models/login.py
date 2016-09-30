from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from flask_login import login_required, login_user, logout_user

from flask import redirect

from werkzeug.security import check_password_hash

from Noteworthington import app, login_manager

import hashlib, binascii, os


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()


class User():
    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, salt, password):
        return password_hash == User.hash_password(password, salt)

    @staticmethod
    def hash_password(password, salt, iterations=10000):
        password = password.encode('utf-8')
        salt = salt.encode('utf-8')
        for i in range(iterations):
            password = hashlib.sha512(password + salt).hexdigest().encode('utf-8')
        return password.decode('utf-8')

    @staticmethod
    def register_user(username, password):
        salt = binascii.hexlify(os.urandom(64)).decode('utf-8')
        password = User.hash_password(password, salt)
        app.config['USERS_COLLECTION'].insert({'username': username, 'password': password, 'salt': salt})


def login(form):
    user = app.config['USERS_COLLECTION'].find_one({"username": form.username.data})
    if user and User.validate_login(user['password'], user['salt'], form.password.data):
        user_obj = User(user['username'])
        login_user(user_obj)
        return True
    return False


@login_manager.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"username": username})
    if not u:
        return None
    return User(username)

