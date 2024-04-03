import sqlite3
import os
from UserLogin import UserLogin
from flask import Flask, render_template, request, flash, g, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from FDataBase import FDataBase
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user
from templates.forms import LoginForm
from models import *

DATABASE = '/tmp/mydb.db'
DEBUG = True
MAX_CONTENT_LENGTH = 1024 * 1024

HOST_NAME = "localhost"
HOST_PORT = 80
app = Flask(__name__, static_folder='static')
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'mydb.db')))

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


Session = sessionmaker(bind=engine)
session = Session()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None
@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route("/")
def main():
    return render_template('main_page.html')

@app.route("/ShowTeachers")
def index():
    teachers = session.query(Teacher).all()
    return render_template('teachers.page.html', teachers=teachers)

@app.route('/redirect', methods=['GET'])
def redirect_page():
    return redirect('/login') # перенаправляем на другую страницу

@app.route('/schedule')
def schedule():
    return render_template('/schedule.html')

@app.route('/<int:teacher_id>')
def view_teacher(teacher_id):
    teacher = session.query(Teacher).get(teacher_id)
    return render_template('teacher.html', teacher=teacher)

@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.getUserByEmail(form.email.data)
        if user and check_password_hash(user['psw'], form.psw.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))

        flash("Неверная пара логин/пароль", "error")

    return render_template("log_page.html", menu=dbase.getMenu(), title="Авторизация", form=form)



@app.route("/profile")
@login_required
def profile():
    return render_template("cabinet.html", menu=dbase.getMenu(), title="Профиль")


@app.route("/teachers/new", methods=['GET', 'POST'])
def newTeacher():
    if request.method == 'POST':
        newTeacher = Teacher(name=request.form['fio'])
        session.add(newTeacher)
        session.commit()
        return redirect(url_for('showTeachers'))
    else:
        return render_template('newTeacher.html', title="information")

@app.route("/teachers/<int:teachers_id>/edit", methods=['POST', 'GET'])
def editTeacher(teacher_id):
    editedTeacher = session.query(Teacher).filtered_by(id=teacher_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedTeacher.title = request.form['name']
            return redirect(url_for('showTeachers'))
    else:
        return render_template('editTeacher.html', teacher=editedTeacher)


if __name__ == "__main__":
    app.run(debug=True)
