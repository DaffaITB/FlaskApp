from flask import Flask
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return "<h1>Home Page</h1>"
    return "<h3>Bottom text</h3>"   #THIS LINE NOT SHOWED UP?

@app.route("/about")
def about():
    return "<h1>About this page</h1><h4>blablablablabla</h4>"

if __name__ == "__main__":
    app.run(debug=True)