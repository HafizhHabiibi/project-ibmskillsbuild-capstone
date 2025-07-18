from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Todo, db
from flask import abort

main = Blueprint('main', __name__)

@main.route('/')
def root_redirect():
    return redirect(url_for('main.login'))

# route ke register
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
@main.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['loggedin'] = True
            session['id'] = user.id
            session['username'] = user.username

            flash('Berhasil login', 'success')
            return redirect(url_for('main.todo'))

        else:
            flash('Password tidak valid', 'danger')
    return render_template('login.html')

# route ke log out
@main.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    flash('Berhasil logout', 'success')
    return redirect(url_for('main.login'))

# route ke todoapp
@main.route('/todo')
def todo():
    if 'loggedin' not in session:
        flash('Silahkan login untuk mengakses halaman ini', 'warning')
        return redirect(url_for('main.login'))
    
    user_id = session['id']
    user_todo = Todo.query.filter_by(user_id=user_id).order_by(Todo.create_at.desc()).all()
    return render_template('todo.html', todo=user_todo)

# route tambah todo
@main.route('/add', methods=['POST'])
def add():
    if 'loggedin' not in session:
        flash('Silahkan login terlebih dahulu', 'warning')
        return redirect(url_for('main.login'))
    
    task = request.form.get('task')
    if not task:
        flash('Task tidak boleh kosong!', 'danger')
        return redirect(url_for('main.todo'))
    
    user_id = session.get('id')
    new_todo = Todo(task=task, user_id=user_id)

    db.session.add(new_todo)
    db.session.commit()

    flash('Task berhasil ditambahkan!', 'success')
    return redirect(url_for('main.todo'))

# route hapus todo
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