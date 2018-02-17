from flask import Flask, jsonify, render_template, request, redirect, url_for
from utils.db import readdb, writedb
from utils.register import RegistrationForm, register_user

app = Flask(__name__)

@app.route('/hello')
def hello():
    return render_template('hello_child.html', value='Hello World')

@app.route('/user/<username>', methods=['GET'])
def user(username):
    user = readdb('users').get(username)
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
            email=form.email.data))
        # TODO - make sure register_user sees the registration data
        return redirect(url_for('user', username=form.username.data))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.debug = True
    app.run()
