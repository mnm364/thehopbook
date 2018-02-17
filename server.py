from flask import Flask

app = Flask(__name__)

# TODO - render "Hello World" at extension /hello

if __name__ == '__main__':
    app.debug = True
    app.run()
