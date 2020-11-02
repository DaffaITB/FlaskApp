from flask import Flask, render_template
app = Flask(__name__)

data_post = [
    {
        "Judul"     : "Postingan pertama ku",
        "Nama"      : "Muhammad Daffa Rasyid",
        "Isi"       : "Saat ini aku sedang mengerjakan tugas PengKom",
        "Tanggal"   : "28 Oktober 2020"
    },
    {
        "Judul"     : "Postingan kedua ku",
        "Nama"      : "Ancien Heart",
        "Isi"       : "*sedang memainkan tablet*",
        "Tanggal"   : "Tidak diketahui"
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("02-home2.1.html", title="home", P = data_post)

@app.route("/about")
def about():
    return render_template("02-about2.0.html", title="about")

@app.route("/about/creator")
def creator():
    return render_template("02-aboutcreator2.0.html", title="creator")

if __name__ == "__main__":
    app.run(debug=True)