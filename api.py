import sqlite3
import os
import json
import pprint
import gspread
from oauth2client.service_account import ServiceAccountCredentials
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
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('CRM3K-8d2f44cc1d61.json', scope)

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

@app.route('/export')
def exportDatabase():
    gc = gspread.authorize(credentials)
    wks = gc.open_by_url('https://docs.google.com/spreadsheets/d/15eTaN59uR6VCBGrmJQighCRTK23K9JKE8YLPRS9h0Qs/edit#gid=0').get_worksheet(0)
    wks.update_acell('A1', 'FirstName')
    wks.update_acell('B1', 'LastName')
    wks.update_acell('C1', 'Company')
    wks.update_acell('D1', 'Status')
    wks.update_acell('E1', 'Picture')

    users = container.get_users()
    i = 2
    for user in users:
        wks.update_acell('A' + str(i), user["prenom"])
        wks.update_acell('B' + str(i), user["nom"])
        wks.update_acell('C' + str(i), user["company"])
        wks.update_acell('D' + str(i), user["status"])
        wks.update_acell('E' + str(i), user["picture"])
        i += 1

    return json.dumps({'status': 200})

@app.route('/import')
def importDatabase():
    container.clear_db()
    gc = gspread.authorize(credentials)
    wks = gc.open_by_url('https://docs.google.com/spreadsheets/d/15eTaN59uR6VCBGrmJQighCRTK23K9JKE8YLPRS9h0Qs/edit#gid=0').get_worksheet(0)
    stillAValue = 1
    i = 1
    while stillAValue == 1:
        i += 1
        user = []
        for j in range(1, 6):
            cell = wks.cell(i, j)
            if cell.value == '':
                stillAValue = 0
            else:
                user.append(cell.value)
        if stillAValue == 1:
            container.create_user(user[0], user[1], user[2], user[3], user[4])

    return json.dumps({'status': 200})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)