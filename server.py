from flask import Flask, jsonify
from utils.db import readdb, writedb

app = Flask(__name__)

@app.route('/hello')
def hello():
    # TODO - render hello world template
    return 'Hello World'

@app.route('/user/<username>', methods=['GET'])
def user(username):
    user = readdb('users').get(username)
    friends = readdb('friends').get(username, [])
    user['friends'] = friends
    return jsonify(user)

if __name__ == '__main__':
    app.debug = True
    app.run()
