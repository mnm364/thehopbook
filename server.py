from flask import Flask, jsonify, request, render_template, json, redirect, Session, url_for
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from utils.db import readdb, writedb
from utils.login import LoginForm, validate_user
from utils.register import RegistrationForm, register_user
from models import User

app = Flask(__name__)
app.secret_key = "SECRET-KEY"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    return User(username)

SUCCESS = json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():

        user = validate_user(form.username.data, form.password.data)

        if not user:
            return render_template('login.html', form=form)

        login_user(user)

        return redirect(url_for('user', username=user.id))

    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        register_user(dict(
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
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/user/<username>', methods=['GET'])
@login_required
def user(username):
    user = readdb('users').get(username)
    current_user_friends = readdb('friends').get(current_user.id, [])

    if user is None or (username != current_user.id and username not in current_user_friends):
        return unauthorized(None)

    friends = readdb('friends').get(username, [])
    user['friends'] = friends
    return render_template('profile.html', user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401

@app.route('/user/<username>', methods=['POST'])
def create_user(username):
    user = request.get_json()
    user['username'] = username
    content = readdb('users')
    content[user['username']] = user
    writedb('users', content)

    return SUCCESS

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
