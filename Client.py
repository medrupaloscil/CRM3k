import os
import sqlite3
import sys
from flask import Flask, request, session, g, url_for, abort, flash

class Client:

	def __init__(self, app):
		self.app = app

	def connect_db(self):
	    rv = sqlite3.connect(self.app.config['DATABASE'])
	    rv.row_factory = sqlite3.Row
	    return rv

	def get_db(self):
	    if not hasattr(g, 'sqlite_db'):
	        g.sqlite_db = self.connect_db()
	    return g.sqlite_db

	def get_users(self):
		db = self.get_db()
		cur = db.execute('select prenom, nom, company, status, picture from users order by id desc')
		users = cur.fetchall()
		response = []
		for user in users:
			response.append(dict(user))
		return response

	def create_user(self, name, lastname, company, status, picture):
		db = self.get_db()
		db.execute('insert into users (prenom, nom, company, status, picture) values (?, ?, ?, ?, ?)',
                     [name, lastname, company, status, picture])
		db.commit()
		return 1