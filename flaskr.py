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

@app.route('/')
def home():
    url = baseAPI + "getAllUsers"
    response = urllib.urlopen(url)
    users = json.loads(response.read())
    return render_template('home.html', users=users)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':

        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save("static/images/" + filename)

        user_data = json.dumps({'prenom': request.form['prenom'], 'nom': request.form['nom'], 'company': request.form['company'], 'status': request.form['status'], 'file': filename})
        url = baseAPI + "createUser"
        response = urllib.urlopen(url, user_data)
        status = json.loads(response.read())
        flash(status)
    else:
        flash("An error happend")

    return redirect(url_for('signup'))