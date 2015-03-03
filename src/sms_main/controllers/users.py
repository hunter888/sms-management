from bottle import template, request
import json

def login():
    data = {}
    for item in request.forms:
        print "item" , item, ":", request.forms.get(item)
        data = json.loads(item)

    email = data['email']
    password = data['password']
    retval = {
		     'user' : email,
		     'password' : password
		    }

    return retval
