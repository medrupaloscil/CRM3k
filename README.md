# CRM3k
Little Python CRM for school project
Composed of both an API and a front flask app.

Run flask app
-------

	$ export FLASK_APP=flaskr.py
	$ flask run
	
And acces it with http://127.0.0.1:5000/
  
  
Run API
-------

	$ python api.py

And acces it with http://127.0.0.1:5001/

Calls API
-------

The different calls you can make are:

* /getAllUsers	**return** {{"id": id, "prenom": prenom, "nom": nom, "company": company, "status": status, "picture": picture}, {...}}

* /getOneUser	**receive** {'id': id}, **return** {"id": id, "prenom": prenom, "nom": nom, "company": company, "status": status, "picture": picture}

* /searchUsers **receive** {'query': query} or {"prenom": prenom, "nom": nom, "company": company, "status": status}, **return** {{"id": id, "prenom": prenom, "nom": nom, "company": company, "status": status, "picture": picture}, {...}}

* /createUser **receive** {"prenom": prenom, "nom": nom, "company": company, "status": status, "picture": picture}, **return** {'status': status}

* /updateUser **receive** {"id": id, "prenom": prenom, "nom": nom, "company": company, "status": status}, **return** {'status': status}

* /removeUser **receive** {'id': id}, **return** {'status': status}

* /clearDatabase **return** {'status': status}

* /export **return** {'status': status}

* /import **return** {'status': status}
