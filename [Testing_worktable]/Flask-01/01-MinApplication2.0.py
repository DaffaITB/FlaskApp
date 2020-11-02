from flask import Flask
app = Flask(__name__)

@app.route("/home")
def home():
    return "<h1>Home Page</h1>"
    return "<h3>Bottom text</h3>"   #THIS LINE NOT SHOWED UP?

if __name__ == "__main__":
    app.run(debug=True)