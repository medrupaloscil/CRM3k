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
        f.save("cdn/" + filename)

        url = baseAPI + "createUser"

    return redirect(url_for('home'))