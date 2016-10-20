#!/usr/bin/env python

from __future__ import print_function
import os
import sqlite3
import sys
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'cdn'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()

@app.route('/')
def home():
    db = get_db()
    cur = db.execute('select prenom, nom, company, status, picture from users order by id desc')
    users = cur.fetchall()
    return render_template('home.html', users=users)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/getusers')
def get_users():
    db = get_db()
    cur = db.execute('select prenom, nom, company, status, picture from users order by id desc')
    users = cur.fetchall()
    result = []
    for user in users:
    	result.append({"prenom": user["prenom"], "nom": user["nom"], "company": user["company"], "status": user["status"], "picture": user["picture"]})
    return json.jsonify(result)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':

        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save("cdn/" + filename)

        db = get_db()
        db.execute('insert into users (prenom, nom, company, status, picture) values (?, ?, ?, ?, ?)',
                     [request.form['prenom'], request.form['nom'], request.form['company'], request.form['status'], filename])
        db.commit()
        flash('New user was successfully added')
    return redirect(url_for('home'))