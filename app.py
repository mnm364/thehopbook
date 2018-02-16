from db_helpers import readdb, writedb
from flask import Flask, jsonify, request, render_template, json, flash, redirect, Session, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import Form, BooleanField, StringField, PasswordField, validators

app = Flask(__name__)
app.secret_key = "SECRET-KEY"

SUCCESS = json.dumps({'success':True}), 200, {'ContentType':'application/json'}


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    name = StringField('Name')
    sex = StringField('Sex')
    relationship = StringField('Relationship Status')
    school = StringField('School')
    concentration = StringField('Concentration')
    status = StringField('Status')
    picture_filename = StringField('Profile Photo Filename')
    # picture = FileField(validators=[
    #     FileRequired(),
    #     FileAllowed(['jpg', 'png'], 'Images only!')])

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/db')
def db(): pass

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        _create_user(dict(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            name=form.name.data,
            sex=form.sex.data,
            relationship=form.relationship.data,
            school=form.school.data,
            concentration=form.concentration.data,
            status=form.status.data,
            picture_filename=form.picture_filename.data))
        flash('Thanks for registering')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/user/<username>', methods=['GET'])
def display_user(username):
    user = readdb('users').get(username)

    if user is None:
        return page_not_found(None)

    friends = readdb('friends').get(username, [])
    user['friends'] = friends
    # return jsonify(user)
    return render_template('profile.html', user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/user/<username>', methods=['POST'])
def create_user(username):
    user = request.get_json()
    user['username'] = username
    _create_user(user)

    return SUCCESS

def _create_user(user):
    # if 'picture' in user:
    #     picture.save(os.path.join(
    #         'db', 'profilepics', username))
    #     user['picture'] = user['picture'].name

    content = readdb('users')
    content[user['username']] = user
    writedb('users', content)

@app.route('/createfriend', methods=['POST'])
def create_friend():
    content = readdb('friends')
    friends = request.form
    from_friends = set(content.setdefault(friends['from'], []))
    from_friends.add(friends['to'])
    to_friends = set(content.setdefault(friends['to'], []))
    to_friends.add(friends['from'])
    content[friends['from']] = list(from_friends)
    content[friends['to']] = list(to_friends)

    writedb('friends', content)

    return SUCCESS

@app.route('/removefriend', methods=['POST'])
def remove_friend():
    content = readdb('friends')
    friends = request.form
    from_friends = set(content.setdefault(friends['from'], []))
    from_friends.remove(friends['to'])
    to_friends = set(content.setdefault(friends['to'], []))
    to_friends.remove(friends['from'])
    content[friends['from']] = list(from_friends)
    content[friends['to']] = list(to_friends)
    writedb('friends', content)

    return SUCCESS

if __name__ == '__main__':
    app.debug = True
    app.run()
