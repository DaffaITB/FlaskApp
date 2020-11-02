from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("02-home1.1.html")

@app.route("/about")
def about():
    return render_template("02-about1.0.html")

@app.route("/about/creator")
def creator():
    return render_template("02-aboutcreator1.0.html")

if __name__ == "__main__":
    app.run(debug=True)