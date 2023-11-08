import os
import sqlite3
from flask import Flask, render_template, flash, abort, redirect, url_for, \
                session, request, g
from decouple import config
from FDataBase import FDataBase

# DBMS configuation
DATABASE = config('DATABASE')
DEBUG = config('DEBUG')
SECRET_KEY = config('SECRET_KEY')

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


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
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())


@app.route('/add_post', methods=['POST', 'GET'])
def add_post():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post'])  > 10:
            res = dbase.addPost(request.form['name'], request.form['post'],  request.form['url'])
            if not res:
                flash('Error adding article', category='error')
            else:
                flash('Article added successfully', category='success')
        else:
            flash('Error adding article', category='error')

    return  render_template('add_post.html', menu=dbase.getMenu(), \
            title='Adding article')


@app.route("/post/<alias>")
def show_post(alias):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.getMenu(), \
                            title=title, post=post)


@app.route('/about')
def about():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('about.html', title='The About Page', menu=dbase.getMenu())


@app.route('/add_feedback', methods=['POST', 'GET'])
def add_feedback():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == 'POST':
        if len(request.form['username']) > 2:
            res = dbase.addFeedback(request.form['username'], request.form['email'], request.form['message'])
            if not res:
                flash('Error adding feedback', category='error')
            else:
                flash('Feedback added successfully', category='success')
        else:
            flash('Error adding feedback', category='error')

    return  render_template('add_feedback.html', menu=dbase.getMenu(), \
            title='Adding feedback')


@app.route('/feedbacks')
def feedbacks():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('feedbacks.html', menu=dbase.getMenu(), feedbacks=dbase.getFeedbacksAnonce())


@app.route('/login', methods=['POST', 'GET'])
def login():
    db = get_db()
    dbase = FDataBase(db)
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and \
        request.form['username'] == "admin" and \
        request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title='Authorization', menu=dbase.getMenu())


@app.errorhandler(404)
def page_not_found(error):
    return  render_template('page404.html', title='Page not found'), 404


@app.teardown_appcontext
def close_db(error):
    """Closes connection with a DBMS if it has been established."""
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == "__main__":
    app.run(debug=True)
