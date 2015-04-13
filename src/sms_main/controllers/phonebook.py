from bottle import template, request
import json
from controllers import lib



class PhoneBook:
    def __init__(self, config):
        self.db_config = config
        self.table = "phonebook"

    def getInfo (self, data):
        temp = { 
            'id' : data[0],
            'department' : data[1],
            'name' : data[2],
            'primary_number' : data[3],
            'secondary_number' : data[4],
            'rank' : data[5],
            'designation' : data[6],
            'home_address' : data[7],
            'user_created' : data[8],
            'date_created' : lib.convertDate(data[9]),
            'user_updated' : data[10],
            'date_updated' : lib.convertDate(data[11]),
            'telco' : data[12],
        }
        return temp

    def all(self):
        query_string = "SELECT * FROM %s" % self.table
        db_data = lib.queryDB(self.db_config, query_string)
       
        data_list = []
        for data in db_data:
            print data
            temp_data = self.getInfo(data)
            data_list.append(temp_data)
        return json.dumps(data_list)

    def get(self, _id):
        query_string = "SELECT * FROM %s WHERE id=%s" % (self.table,str(_id))
        db_data = lib.queryDB(self.db_config, query_string)
       
        data_list = []
        for data in db_data:
            temp_data = self.getInfo(data)
            data_list.append(temp_data)

        return json.dumps(data_list)

    def delete (self, _id):
        print "inbox_id", _id
        query_string = "DELETE FROM %s WHERE id=%s" % (self.table, str(_id))
        lib.execDB(self.db_config, query_string)

        retval = {
            'success' : 'true'
        }

        return retval

    def verify_number (self, number):
        print "[verify_number] ", len(number)
        if (len(number) == 11) :
            return 1
        else:
            return 0

    def create(self):
        retval = {
            'success' : 'false'
        }
        department = request.query.department
        name = request.query.name
        primary_number = request.query.mobile_number
        rank = request.query.rank
        designation = request.query.designation
        home_address = request.query.home_address

        if (self.verify_number(str(primary_number)) == 0):
            retval['field'] = "mobile_number"
            return retval
        query_string = "INSERT INTO %s (department, name," % self.table
        query_string += " primary_number, rank, designation, home_address) VALUES "
        query_string += "('%s', '%s','%s','%s','%s','%s')" % (department, name, primary_number,rank,designation, home_address)
        lib.execDB(self.db_config, query_string)

        retval = {
            'success' : 'true'
        }

        return retval

