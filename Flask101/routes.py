import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from Flask101 import app, db, bcrypt, login_manager
from Flask101.forms import form_registrasi, form_login, form_perbaruiakun, form_pos
from Flask101.models import user, post
from flask_login import login_user, logout_user, current_user, login_required

pos_awal = [
    {
        "Judul"     : "Postingan pertama ku",
        "author"      : "Muhammad Daffa Rasyid",
        "Isi"       : "Saat ini aku sedang mengerjakan tugas PengKom",
        "Tanggal"   : "28 Oktober 2020"
    },
    {
        "Judul"     : "Postingan kedua ku",
        "author"      : "Ancien Heart",
        "Isi"       : "*sedang memainkan tablet*",
        "Tanggal"   : "Tidak diketahui"
    }
]

@app.route("/")
@app.route("/beranda")
def beranda():
    #data_post = post.query.all() # + pos_awal
    halaman = request.args.get('page', 1, type=int)
    pos_berurut = post.query.order_by(post.Tanggal.desc()).paginate(page=halaman, per_page=5)
    return render_template("home1.1.html", title="beranda", pos = pos_berurut)

@app.route("/tentang",)
def tentang():
    return render_template("about1.0.html", title="tentang")

@app.route("/tentang/pengembang")
def pengembang():
    return render_template("aboutcreator1.0.html", title="tentang/pengembang")

@app.route("/daftar", methods = ["GET", "POST"])
def daftar():
    if current_user.is_authenticated:
        return redirect(url_for("beranda"))
    daftar = form_registrasi()
    if daftar.validate_on_submit():
        password_enkripsi = bcrypt.generate_password_hash(daftar.password.data).decode("utf-8")
        pengguna_baru = user(username=daftar.username.data, email=daftar.email.data, password=password_enkripsi)
        db.session.add(pengguna_baru)
        db.session.commit()
        flash(f"Akun {daftar.username.data} berhasil dibuat! Silakan masuk untuk lanjut.", "success")
        logout_user()
        return redirect(url_for("masuk"))
    return render_template("register1.0.html", title="daftar", form = daftar)

@app.route("/masuk", methods = ["GET", "POST"])
def masuk():
    if current_user.is_authenticated:
        return redirect(url_for("beranda"))
    masuk = form_login()
    if masuk.validate_on_submit():
        user_tersedia = user.query.filter_by(email=masuk.email.data).first()
        if user_tersedia and bcrypt.check_password_hash(user_tersedia.password, masuk.password.data):
            login_user(user_tersedia, remember=masuk.remember_account.data)
            lanjut = request.args.get("next")
            flash(f"Selamat datang {current_user.username}!", "success")
            return redirect(lanjut) if lanjut else redirect(url_for("beranda"))
        else:
            flash("Tidak dapat masuk, silakan cek kembali email dan password Anda!", "danger")
    return render_template("login1.0.html", title="masuk", form = masuk)

@app.route("/keluar")
def keluar():
    logout_user()
    return redirect(url_for("masuk"))


def foto_baru(form_fotouser):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_fotouser.filename)
    nama_file = random_hex + f_ext
    lokasi_file = os.path.join(app.root_path, 'static/gambar/foto user', nama_file)

    besarnya_data = (125, 125)
    i = Image.open(form_fotouser)
    i.thumbnail(besarnya_data)
    i.save(lokasi_file)

    return nama_file

@app.route("/akun", methods=["GET", "POST"])
@login_required
def akun():
    perbarui = form_perbaruiakun()
    if perbarui.validate_on_submit():
        if perbarui.picture.data:
            picture_file = foto_baru(perbarui.picture.data)
            current_user.profile_picture = picture_file
        current_user.username = perbarui.username.data
        current_user.email = perbarui.email.data
        db.session.commit()
        flash("Akun berhasil diperbarui!", "success")
        return redirect(url_for('akun'))
    elif request.method == 'GET':
        perbarui.username.data = current_user.username
        perbarui.email.data = current_user.email
    foto_user = url_for("static", filename="gambar/foto user/" + current_user.profile_picture)
    return render_template("account1.0.html", title="akun", fotonya_user=foto_user, form=perbarui)

@app.route("/pos/baru", methods=["GET", "POST"])
@login_required
def pos_baru():
    pos = form_pos()
    if pos.validate_on_submit():
        pos = post(Judul=pos.title.data, Isi=pos.content.data, author=current_user)
        db.session.add(pos)
        db.session.commit()
        flash("Pos berhasil diunggah", "success")
        return redirect(url_for("beranda"))
    return render_template("createpost1.0.html", title="pos baru", form = pos, legend="Pos Baru")

@app.route("/pos/<int:pos_id>")
def pos(pos_id):
    pos = post.query.get_or_404(pos_id)
    return render_template("pos1.0.html", title=pos.Judul, post = pos)

@app.route("/pos/<int:pos_id>/perbarui", methods=["GET", "POST"])
@login_required
def pos_perbarui(pos_id):
    pos = post.query.get_or_404(pos_id)
    if pos.author != current_user:
        abort(403)
    perbarui = form_pos()
    if perbarui.validate_on_submit():
        pos.Judul = perbarui.title.data
        pos.Isi = perbarui.content.data
        db.session.commit()
        flash("Pos berhasil diperbarui", "success")
        return redirect(url_for("pos", pos_id=pos.id))
    elif request.method == "GET":
        perbarui.title.data = pos.Judul
        perbarui.content.data = pos.Isi
    return render_template("createpost1.0.html", title="perbarui pos", form = perbarui, legend="Perbarui Pos")

@app.route("/pos/<int:pos_id>/hapus", methods=["POST"])
@login_required
def pos_hapus(pos_id):
    pos = post.query.get_or_404(pos_id)
    if pos.author != current_user:
        abort(403)
    db.session.delete(pos)
    db.session.commit()
    flash("Pos berhasil dihapus", "warning")
    return redirect(url_for("beranda"))

@app.route("/pengguna/<string:username>")
def pos_pengguna(username):
    page = request.args.get('page', 1, type=int)
    pengguna = user.query.filter_by(username=username).first_or_404()
    postingan_pengguna = post.query.filter_by(author=pengguna)\
        .order_by(post.Tanggal.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts1.0.html', pos=postingan_pengguna, user=pengguna)