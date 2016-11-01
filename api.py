import sqlite3
import os
import json
import pprint
from flask import Flask, jsonify, g, request
from Client import Client


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

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

@app.route('/getAllUsers', methods=['GET'])
def getAllUsers():
    return json.dumps(container.get_users())

@app.route('/createUser', methods=['POST'])
def createUser():
    datas = json.loads(request.get_data())
    container.create_user(datas['prenom'], datas['nom'], datas['company'], datas['status'], datas['file'])
    return json.dumps({'status': 200})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)