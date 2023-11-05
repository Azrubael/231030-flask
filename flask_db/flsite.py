import os
import sqlite3
from flask import Flask, render_template, request, g
from decouple import config

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

    # declaration to ensure that records are returned from the database as dictionaries rather than tuples
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
    return render_template('index.html', menu = [])


@app.teardown_appcontext
def close_db(error):
    """Closes connection with a DBMS if it has been established."""
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == "__main__":
    app.run(debug=True)
