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

@app.route('/getOneUser', methods=['POST'])
def getOneUser():
    datas = json.loads(request.get_data())
    if 'id' in datas:
        return json.dumps(container.get_user_pk(datas["id"]))
    else:
        return json.dumps({'status': 500, 'message': "Missing arguments"})

@app.route('/createUser', methods=['POST'])
def createUser():
    datas = json.loads(request.get_data())
    if 'prenom' in datas and 'nom' in datas and 'company' in datas and 'status' in datas and 'file' in datas:
        container.create_user(datas['prenom'], datas['nom'], datas['company'], datas['status'], datas['file'])
        return json.dumps({'status': 200})
    else:
        return json.dumps({'status': 500, 'message': "Missing arguments"})

@app.route('/updateUser', methods=['POST'])
def updateUser():
    datas = json.loads(request.get_data())
    if 'id' in datas and 'prenom' in datas and 'nom' in datas and 'company' in datas and 'status' in datas:
        container.update_user(datas['id'],datas['prenom'], datas['nom'], datas['company'], datas['status'])
        return json.dumps({'status': 200})
    else:
        return json.dumps({'status': 500, 'message': "Missing arguments"})

@app.route('/removeUser', methods=['POST'])
def removeUser():
    datas = json.loads(request.get_data())
    if 'id' in datas:
        container.remove_user(datas['id'])
        return json.dumps({'status': 200})
    else:
        return json.dumps({'status': 500, 'message': "Missing arguments"})

@app.route('/clearDatabase')
def clearDatabase():
    container.clear_db()
    return json.dumps({'status': 200})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)