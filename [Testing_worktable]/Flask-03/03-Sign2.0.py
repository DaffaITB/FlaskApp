from flask import Flask, render_template, url_for, flash, redirect
from forms import form_registrasi, form_login
app = Flask(__name__)

app.config["SECRET_KEY"] = "thisismysecretkey101"

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
    return render_template("03-login1.0.html", title="masuk", form = masuk)

@app.route("/tentang",)
def tentang():
    return render_template("03-about1.0.html", title="tentang")

@app.route("/tentang/pengembang")
def pengembang():
    return render_template("03-aboutcreator1.0.html", title="tentang/pengembang")

if __name__ == "__main__":
    app.run(debug=True)