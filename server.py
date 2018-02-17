from flask import Flask, jsonify, render_template
from utils.db import readdb, writedb

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

if __name__ == '__main__':
    app.debug = True
    app.run()
