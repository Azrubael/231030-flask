# Updates for application 'flsite_deco.py'.

import os
import sqlite3
from flask import Flask, render_template, flash, abort, redirect, url_for, \
                session, request, g
from decouple import config
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user
from FDataBase import FDataBase
from UserLogin import UserLogin


# DBMS configuation
DATABASE = config('DATABASE')
DEBUG = config('DEBUG')
SECRET_KEY = config('SECRET_KEY')

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

login_namager = LoginManager(app)


@login_namager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromBD(user_id, g.dbase)


def connect_db():
    """Establishing a connection to the database."""
    conn= sqlite3.connect(app.config['DATABASE'])

    # to ensure that records are returned from the database as dictionaries rather than tuples
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """Auxiliary function for creating a database and a tables inside it without running a web server."""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Establishes a connection with a DBMS if there is no connection yet."""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route("/")
def index():
    return render_template('index.html', menu=g.dbase.getMenu(), \
                        posts=g.dbase.getPostsAnonce())


@app.route('/add_post', methods=['POST', 'GET'])
def add_post():

    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post'])  > 10:
            res = g.dbase.addPost(request.form['name'], \
                            request.form['post'],  request.form['url'])
            if not res:
                flash('Error adding article', category='error')
            else:
                flash('Article added successfully', category='success')
        else:
            flash('Error adding article', category='error')

    return  render_template('add_post.html', menu=g.dbase.getMenu(), \
            title='Adding article')


@app.route("/post/<alias>")
@login_required
def show_post(alias):
    title, post = g.dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('post.html', menu=g.dbase.getMenu(), \
                        title=title, post=post)


@app.route('/about')
def about():
    return render_template('about.html', title='The About Page', \
                        menu=g.dbase.getMenu())


@app.route('/add_feedback', methods=['POST', 'GET'])
def add_feedback():

    if request.method == 'POST':
        if len(request.form['username']) > 2:
            res = g.dbase.addFeedback(request.form['username'], request.form['email'], request.form['message'])
            if not res:
                flash('Error adding feedback', category='error')
            else:
                flash('Feedback added successfully', category='success')
        else:
            flash('Error adding feedback', category='error')

    return  render_template('add_feedback.html', menu=g.dbase.getMenu(), \
            title='Adding feedback')


@app.route('/feedbacks')
@login_required
def feedbacks():
    return render_template('feedbacks.html', menu=g.dbase.getMenu(), \
                        feedbacks=g.dbase.getFeedbacksAnonce())


@app.route('/login', methods=['POST', 'GET'])
def login():
    print("LOGIN REQUEST >>>", request.form)
    if request.method == 'POST':
        user = g.dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userLogin = UserLogin().create(user)
            login_user(userLogin)
            return redirect(url_for('index'))
        flash("Wrong pair login/password", "error")

    return render_template('login.html', title='Authorization', \
                        menu=g.dbase.getMenu())


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if len(request.form['username']) > 3 and \
                len(request.form['email']) > 4 and \
                len(request.form['psw']) > 3 and \
                request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = g.dbase.addUser(request.form['username'], \
                                request.form['email'], hash)
            if res:
                flash("You are successfully registered", "success")
                return redirect(url_for('login'))
            else:
                flash("Error when adding a user to the DataBase", "error")
        else:
            flash("Fields are filled incorrectly")

    return render_template('register.html', menu=g.dbase.getMenu(), \
                        title="Authorization")


@app.errorhandler(404)
def page_not_found(error):
    return  render_template('page404.html', title='Page not found'), 404


@app.before_request
def before_request():
    print("before_request() called")
    if request.endpoint not in ["static_root","static"]:
        # `static()` это внутренняя функция Flask
        db = get_db()
        g.dbase = FDataBase(db)


@app.after_request
def after_request(response):
    print("after_request() called")
    return response


@app.teardown_request
def teardown_request(response):
    """Closes connection with a DBMS if it has been established."""
    print("after_request() called")
    if hasattr(g, 'link_db'):
        g.link_db.close()
    return response


if __name__ == "__main__":
    app.run(debug=True)

# Flask 15 [timecode 06:25]