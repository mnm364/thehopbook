from wtforms import Form, BooleanField, StringField, PasswordField, validators
from utils.db import readdb, writedb

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

    # TODO - add fields (name, sex, relationship, school, concentration,
    #        status, picture_filename)

def register_user(user):
    content = readdb('users')
    content[user['username']] = user
    writedb('users', content)
