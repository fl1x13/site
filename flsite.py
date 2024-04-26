import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, g, flash, make_response

from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin

DATABASE = '/instance/flsite.db'
DEBUG = True
SECRET_KEY = 'development key'
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизуйтесь для доступа к контенту'
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    print("Load_user")
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route('/')
def index():
    cars = dbase.get_cars()
    return render_template('index.html', menu=dbase.getMenu(), data=cars)


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == "POST":
        res = dbase.create(request.form['title'], request.form['price'], request.form['description'])

    return render_template('create.html', menu=dbase.getMenu(), title='Добавление машины')


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get('next') or url_for('profile'))
        flash('Неверный логин или пароль', 'error')

    return render_template('login.html', menu=dbase.getMenu(), title='Авторизация')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == "POST":
        if len(request.form['name']) > 4 and request.form['password'] == request.form['password_confirm']:
            hash = generate_password_hash(request.form['password'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash('Вы успешно зарегистрировались', 'success')
                return redirect(url_for('index'))
            else:
                flash('Ошибка при добавлении в базу данных', 'error')
        else:
            flash('Неверно заполненны поля', 'error')
    return render_template('register.html', menu=dbase.getMenu(), title='Регистрация')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из профиля', 'success')
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', menu=dbase.getMenu(), title='Профиль')


@app.route('/userava')
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash('Ошибка обновления аватара', 'error')
                    return redirect(url_for('profile'))
                flash('Аватар успешно обновлен', 'info')
            except FileNotFoundError as e:
                flash('Файл не найден', 'error')
        else:
            flash('Ошибка обновления аватара', 'error')
    return redirect(url_for('profile'))


@app.route('/buy', methods=['POST', 'GET'])
@login_required
def buy():
    return render_template('buy.html')


if __name__ == '__main__':
    app.run(debug=True)
