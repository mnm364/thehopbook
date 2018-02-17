from wtforms import Form, StringField, PasswordField
from models import User
from utils.db import readdb, writedb


class LoginForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')

def validate_user(username, password):
    users = readdb('users')
    user_dict = users.get(username)

    if user_dict is None or user_dict['password'] != password:
        return None

    return User(username)
