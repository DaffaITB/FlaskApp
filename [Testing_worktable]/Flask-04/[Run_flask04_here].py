from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import form_registrasi, form_login

app = Flask(__name__)
app.config["SECRET_KEY"] = "thisismysecretkey101"
app.config["SQLALCHEMY_DATABASES_URI"] = "sqlite:///flask.db"
db = SQLAlchemy(app)

class user(db.Model):
    id              = db.column(db.integer, primary_key=True)
    username        = db.column(db.String(20), nullable=False, unique=True,)
    email           = db.column(db.String(99), nullable=False, unique=True,)
    password        = db.column(db.String(50), nullable=False)
    profile_picture = db.column(db.String(20), nullable=False, default="default.jpg")
    data_post       = db.relationship("post", backref="author", lazy=True)

    def __repr__(self):
        return f"user('{self.username}', '{self.email}', '{self.profile_picture}')"

class post(db.Model):
    id      = db.column(db.Integer, primary_key=True)
    Judul   = db.column(db.String(99), nullable=False)
    Isi     = db.column(db.String(db.Text), nullable=False)
    Tanggal = db.column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.column(db.Integer, nullable=False, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"user('{self.Judul}', '{self.Tanggal}')"

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
@app.route("/beranda")
def beranda():
    return render_template("03-home1.0.html", title="beranda", P = data_post)

@app.route("/daftar", methods = ["GET", "POST"])
def daftar():
    daftar = form_registrasi()
    if daftar.validate_on_submit():
        flash(f"Akun {daftar.username.data} berhasil dibuat!", "success")
        return redirect(url_for("beranda"))
    return render_template("03-register1.0.html", title="daftar", form = daftar)

@app.route("/masuk", methods = ["GET", "POST"])
def masuk():
    masuk = form_login()
    if masuk.validate_on_submit():
        if masuk.email.data == "ancienheart@gmail.com" and masuk.password.data == "ancien26":
            flash("Selamat datang kembali [ceritanya username]!", "success")
            return redirect(url_for("beranda"))
        else:
            flash("Akun tidak terdaftar, silakan cek kembali email dan password Anda!", "danger")
    return render_template("03-login1.0.html", title="masuk", form = masuk)

@app.route("/tentang",)
def tentang():
    return render_template("03-about1.0.html", title="tentang")

@app.route("/tentang/pengembang")
def pengembang():
    return render_template("03-aboutcreator1.0.html", title="tentang/pengembang")

if __name__ == "__main__":
    app.run(debug=True)