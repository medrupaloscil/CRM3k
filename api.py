import sqlite3
import os
import json
from flask import Flask, jsonify, g
from Client import Client


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

container = Client(app)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = container.get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()

@app.route('/', methods=['GET'])
def api():
	return "Hello World !"

@app.route('/getAllUsers', methods=['GET', 'POST'])
def getAllUsers():
    return json.dumps(container.get_users())

@app.route('/createUser')
def createUser():
	container.create_user(request.form['prenom'], request.form['nom'], request.form['company'], request.form['status'], filename)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)