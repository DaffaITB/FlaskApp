from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Hello, World!<h1>\nUwUwUwU</h1>OwOwOwO"