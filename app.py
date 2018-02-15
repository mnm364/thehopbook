from flask import Flask, jsonify, request
import simplejson as json

app = Flask(__name__)

SUCCESS = json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/')
def index():
    return 'Welcome to [thehopbook]'

@app.route('/user/<username>', methods=['GET'])
def display_user(username):
    with open('nosqldb/users.json', 'r') as f, open('nosqldb/friends.json', 'r') as g:
        user = json.loads(f.read()).get(username)
        friends = json.loads(g.read()).get(username, [])
        user['friends'] = friends
        return jsonify(user)

@app.route('/user/<username>', methods=['POST'])
def create_user(username):
    with open('nosqldb/users.json', 'r+') as f:
        content = json.loads(f.read())
        content[username] = request.get_json()
        f.seek(0)
        f.write(json.dumps(content, sort_keys=True, indent=2, separators=(',', ': ')))
        f.truncate()

    return SUCCESS

@app.route('/createfriend', methods=['POST'])
def create_friend():
    with open('nosqldb/friends.json', 'r+') as f:
        content = json.loads(f.read())
        friends = request.form
        from_friends = set(content.setdefault(friends['from'], []))
        from_friends.add(friends['to'])
        to_friends = set(content.setdefault(friends['to'], []))
        to_friends.add(friends['from'])
        content[friends['from']] = list(from_friends)
        content[friends['to']] = list(to_friends)

        f.seek(0)
        f.write(json.dumps(content, sort_keys=True, indent=2, separators=(',', ': ')))
        f.truncate()

    return SUCCESS

@app.route('/removefriend', methods=['POST'])
def remove_friend():
    with open('nosqldb/friends.json', 'r+') as f:
        content = json.loads(f.read())
        friends = request.form
        from_friends = set(content.setdefault(friends['from'], []))
        from_friends.remove(friends['to'])
        to_friends = set(content.setdefault(friends['to'], []))
        to_friends.remove(friends['from'])
        content[friends['from']] = list(from_friends)
        content[friends['to']] = list(to_friends)

        f.seek(0)
        f.write(json.dumps(content, sort_keys=True, indent=2, separators=(',', ': ')))
        f.truncate()

    return SUCCESS

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

