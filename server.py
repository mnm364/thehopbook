from flask import Flask, jsonify, render_template, request, redirect, url_for
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

@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/hello')
def hello():
    return render_template('hello_child.html', value='Hello World')

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

        return redirect(url_for('user', username=form.username.data))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.debug = True
    app.run()
