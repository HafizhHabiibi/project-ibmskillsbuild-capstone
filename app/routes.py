from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Todo, db
from flask import abort

main = Blueprint('main', __name__)

@main.route('/')
# Fungsi route yang mengarahkan pengguna ke halaman login saat mereka mengakses root URL ('/').
def root_redirect():
    return redirect(url_for('main.login'))

# route ke register
# Route ini digunakan untuk proses registrasi pengguna dalam aplikasi web.
@main.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # valisdasi username unik atau tidak
        existing_username = User.query.filter_by(username=username).first()

        if existing_username:
            flash('Username ini sudah terdaftar, silahkan masukan username lain.', 'danger')
            return redirect(url_for('main.register'))
        
        # hashing password saat user register
        hashed_password = generate_password_hash(password)

        # simpon data baru dengan SQLAlchemy
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registrasi berhasil dilakukan silahkan login!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')
    
# route ke login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Mengambil data username dan password dari form submission
        username = request.form['username']
        password = request.form['password']

        # Mencoba mencari pengguna berdasarkan username di database
        user = User.query.filter_by(username=username).first()

        # Jika pengguna ditemukan dan password valid, login berhasil
        if user and check_password_hash(user.password_hash, password):
            # Menambahkan informasi login ke dalam session
            session['loggedin'] = True
            session['id'] = user.id
            session['username'] = user.username

            # Mengirimkan pesan sukses dan mengarahkan ke halaman to-do
            flash('Berhasil login', 'success')
            return redirect(url_for('main.todo'))

        # Jika pengguna tidak ditemukan atau password salah, tampilkan pesan error
        else:
            flash('Password tidak valid', 'danger')
    # Jika itu adalah request GET (biasanya saat pertama kali load halaman),
    # menampilkan form login
    return render_template('login.html')

# route ke log out
@main.route('/logout')
#Fungsi ini, `logout()`, adalah route Flask yang digunakan untuk menghilangkan sessi pengguna saat mereka keluar dari aplikasi.
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('main.login'))

# route ke todoapp
@main.route('/todo')
def todo():
    # Cek apakah pengguna sudah login
    if 'loggedin' not in session:
        # Jika tidak, tampilkan pesan flash dan redirect ke halaman login
        flash('Silahkan login untuk mengakses halaman ini', 'warning')
        return redirect(url_for('main.login'))
    
    # Jika pengguna sudah login, ambil ID pengguna dari session
    user_id = session['id']
    
    # Query database untuk mendapatkan semua to-do yang terkait dengan ID pengguna, sudhah menurunkan berdasarkan waktu pembuatan, dan tampilkan lewat template 'todo.html'
    user_todo = Todo.query.filter_by(user_id=user_id).order_by(Todo.create_at.desc()).all()
    return render_template('todo.html', todo=user_todo)

# route tambah todo
@main.route('/add', methods=['POST'])
def add():
    # Verifikasi apakah pengguna sudah login
    if 'loggedin' not in session:
        flash('Silahkan login terlebih dahulu', 'warning')
        return redirect(url_for('main.login'))
    
    # Ambil data dari form input bernama 'task'
    task = request.form.get('task')
    # Jika task kosong, tampilkan pesan flash dan redirect ke halaman to-do
    if not task:
        flash('Task tidak boleh kosong!', 'danger')
        return redirect(url_for('main.todo'))
    
    # Ambil ID pengguna dari session
    user_id = session.get('id')
    # Buat objek baru Todo dengan task dan user_id
    new_todo = Todo(task=task, user_id=user_id)

    # Tambahkan objek baru ke session dan simpan perubahan
    db.session.add(new_todo)
    db.session.commit()

    # Tampilkan pesan flash berhasil dan redirect ke halaman to-do
    flash('Task berhasil ditambahkan!', 'success')
    return redirect(url_for('main.todo'))

# route hapus todo
# Route '/delete/<id>' untuk menghapus tugas
@main.route('/delete/<int:id>')
def delete(id):
    if 'loggedin' not in session:
        flash('Silahkan login terlebih dulu', 'danger')
        return redirect(url_for('main.login'))

    todo = Todo.query.get_or_404(id)

    # cek apakah task ini milik user login
    if todo.user_id != session['id']:
        abort(403)

    db.session.delete(todo)
    db.session.commit()

    flash('Task berhasil dihapus!', 'success')
    return redirect(url_for('main.todo'))

# route edit task
# Route '/edit/<id>' dalam aplikasi to-do list Flask
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
# Fungsi ini mengelola proses perubahan atau penghapusan tugas (task) yang sudah ada.
def edit(id):
    if 'loggedin' not in session:
        flash('Silahkan login terlebih dulu', 'danger')
        return redirect(url_for('main.login'))
    
    todo = Todo.query.get_or_404(id)

    # pastikan user login yang bisa edit task
    if todo.user_id != session['id']:
        abort(403)

    if request.method == 'POST':
        new_task = request.form.get('task')
        if not new_task:
            flash('Task tidak boleh kosong!', 'danger')
            return redirect(url_for('main.edit', id=id))
        
        todo.task = new_task
        db.session.commit()

        flash('Task berhasil diperbarui', 'success')
        return redirect(url_for('main.todo'))
    
    return render_template('edit.html', todo=todo)