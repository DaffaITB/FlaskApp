from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("02-home1.1.html")

@app.route("/about")
def about():
    return "<h1>About this page</h1><h4>blablablablabla</h4>"

@app.route("/about/creator")
def creator():
    return "<h1>Muhammad Daffa Rasyid</h1><h4>NIM 16520147</h4>"

if __name__ == "__main__":
    app.run(debug=True)