from db_helpers import readdb, writedb
from flask import Flask, jsonify, request, render_template, json, flash, redirect, Session, url_for
from register import RegistrationForm, register_user

app = Flask(__name__)
app.secret_key = "SECRET-KEY"

SUCCESS = json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/')
def index():
    return render_template('login.html')

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
    return render_template('profile.html', user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/user/<username>', methods=['POST'])
def create_user(username):
    user = request.get_json()
    user['username'] = username
    register_user(user)

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
