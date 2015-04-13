from bottle import template, request
import json
from controllers import lib



class Users:
    def __init__(self, config):
        self.db_config = config
        self.table = "users"


    def getInfo (self, data):
        temp = {
            'id' : data[0],
            'username' : data[1],
            'firstname' : data[2],
            'lastname' : data[3],
            'email' : data[4],
            'password' : data[5],
            'role' : data[6],
        }
        return temp


    def login(self):
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

    def create(self):
        for item in request.forms:
            print "item" , item, ":", request.forms.get(item)
            data = json.loads(item)


        confirm_password = request.query.confirm_password
        email = request.query.email
        firstname = request.query.firstname
        lastname = request.query.lastname
        password = request.query.password
        role = request.query.role
        username = request.query.username
        timestamp = lib.getTimeStamp()

        query_string = "INSERT INTO users (username, firstname, lastname,"
        query_string += "email, password, role, timestamp) VALUES "
        query_string += "('%s', '%s','%s','%s','%s','%s','%s')" % (username, firstname, lastname,email, password, role, timestamp)

        print "halloo ", username
        print query_string
        lib.execDB(self.db_config, query_string)
        print "db commit"

        retval = {
		        'success' : 'true'
		    }

        return retval

    def all(self):
        query_string = "SELECT * FROM users"
        db_data = lib.queryDB(self.db_config, query_string)
       
        users = []
        for data in db_data:
            print data
            user = { 
                'id' : data[0],
                'username' : data[1],
                'firstname' : data[2],
                'lastname' : data[3],
            }
            users.append(user)

        return json.dumps(users)

    def get(self, user_id):
        query_string = "SELECT * FROM users WHERE id=%s" % str(user_id)
        db_data = lib.queryDB(self.db_config, query_string)
       
        data_list = []
        for data in db_data:
            print data
            temp_data = self.getInfo(data)
            data_list.append(temp_data)

        return json.dumps(data_list)




