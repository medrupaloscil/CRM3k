#!/usr/bin/env python

from __future__ import print_function
import os
import sqlite3
import sys
import urllib
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

baseAPI = "http://127.0.0.1:5001/"

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def getJSON(url, data = None):
    response = urllib.urlopen(url, data)
    return json.loads(response.read())

@app.route('/')
def home():
    users = getJSON(baseAPI + "getAllUsers")
    return render_template('home.html', users=users)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/admin')
def admin():
    users = getJSON(baseAPI + "getAllUsers")
    return render_template('admin.html', users=users)

@app.route('/user/<user_id>')
def user(user_id):
    data = json.dumps({'id': user_id})
    user = getJSON(baseAPI + "getOneUser", data)
    return render_template('user.html', user=user)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':

        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save("static/images/" + filename)

        user_data = json.dumps({'prenom': request.form['prenom'], 'nom': request.form['nom'], 'company': request.form['company'], 'status': request.form['status'], 'file': filename})
        status = getJSON(baseAPI + "createUser", user_data)
        if status["status"] == 200 :
            flash("User added with success")
        else :
            flash("Error code %i", (status["status"]))
    else:
        flash("An error happend")

    return redirect(url_for('signup'))

@app.route('/removeUser/<user_id>', methods=['GET', 'POST'])
def remove_user(user_id):

    user_data = json.dumps({'id': user_id})
    status = getJSON(baseAPI + "removeUser", user_data)
    if status["status"] == 200 :
        flash("User deleted with success")
    else :
        flash("Error code %i", (status["status"]))

    return redirect(url_for('admin'))

@app.route('/updateUser/<user_id>', methods=['GET', 'POST'])
def update_user(user_id):

    user_data = json.dumps({'id': user_id, 'prenom': request.form['prenom'], 'nom': request.form['nom'], 'company': request.form['company'], 'status': request.form['status']})
    status = getJSON(baseAPI + "updateUser", user_data)
    if status["status"] == 200 :
        flash("User updated with success")
    else :
        flash("Error => %s" % status["message"])

    return redirect(url_for('user', user_id = user_id))

@app.route('/clearDatabase')
def clear_database():
    status = getJSON(baseAPI + "clearDatabase")
    if status["status"] == 200 :
        flash("Users deleted with success")
    else :
        flash("Error code %i", (status["status"]))
    return redirect(url_for('admin'))

@app.route('/export')
def export_database():
    status = getJSON(baseAPI + "export")
    if status["status"] == 200 :
        flash("Database exported")
    else :
        flash("Error")
    return redirect(url_for('admin'))

@app.route('/import')
def import_database():
    status = getJSON(baseAPI + "import")
    if status["status"] == 200 :
        flash("Database imported")
    else :
        flash("Error")
    return redirect(url_for('admin'))