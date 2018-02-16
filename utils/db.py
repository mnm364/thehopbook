from flask import json

def readdb(table):
    with open('db/' + table + '.json', 'r') as f:
        return json.load(f)

def writedb(table, content):
    with open('db/' + table + '.json', 'w') as f:
        f.write(
            json.dumps(
                content,
                sort_keys=True,
                indent=2,
                separators=(',', ': ')))
