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

	def clear_db(self):
		db = self.get_db()
		db.execute('DELETE FROM users WHERE 1')
		db.commit()

	def get_users(self):
		db = self.get_db()
		cur = db.execute('SELECT * FROM users ORDER BY id desc')
		users = cur.fetchall()
		response = []
		for user in users:
			response.append(dict(user))
		return response

	def get_user_pk(self, user_id):
		db = self.get_db()
		cur = db.execute('SELECT * FROM users WHERE id = %s' % user_id)
		users = cur.fetchall()
		response = dict(users[0])
		return response

	def search_users(self, query):
		db = self.get_db()
		cur = db.execute("SELECT * FROM users WHERE prenom='%s' OR nom='%s' OR company='%s' OR status='%s' ORDER BY id desc" % (query, query, query, query))
		users = cur.fetchall()
		response = []
		for user in users:
			response.append(dict(user))
		return response

	def complexe_search_users(self, prenom, nom, company, status):
		req = 'SELECT * FROM users WHERE '

		args = 0

		if prenom != "":
			if args > 0:
				req += "AND "
			args += 1
			req += "prenom = '" + prenom + "' "
		if nom != "":
			if args > 0:
				req += "AND "
			args += 1
			req += "nom = '" + nom + "' "
		if company != "":
			if args > 0:
				req += "AND "
			args += 1
			req += "company = '" + company + "' "
		if status != "":
			if args > 0:
				req += "AND "
			args += 1
			req += "status = '" + status + "' "
		if args == 0:
			req += "1"

		req += "ORDER BY id desc"

		db = self.get_db()
		cur = db.execute(req)
		users = cur.fetchall()
		response = []
		for user in users:
			response.append(dict(user))
		return response

	def create_user(self, name, lastname, company, status, picture):
		db = self.get_db()
		db.execute('INSERT INTO users (prenom, nom, company, status, picture) values (?, ?, ?, ?, ?)',
                     [name, lastname, company, status, picture])
		db.commit()
		return 1

	def update_user(self, user_id, name, lastname, company, status):
		db = self.get_db()
		db.execute('UPDATE users SET prenom = ?, nom = ?, company = ?, status = ? WHERE id = %s' % user_id,
                     [name, lastname, company, status])
		db.commit()
		return 1

	def remove_user(self, user_id):
		db = self.get_db()
		db.execute('DELETE FROM users WHERE id = %s' % user_id)
		db.commit()
		return 1