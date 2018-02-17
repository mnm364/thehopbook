from flask import Flask, jsonify
from utils.db import readdb, writedb

app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'Hello World'

@app.route('/user/<username>', methods=['GET'])
def user(username):
    user = readdb('users').get(username)

    # TODO - add friends to user response

    return jsonify(user)

if __name__ == '__main__':
    app.debug = True
    app.run()
