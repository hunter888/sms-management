from bottle import template, request
import json
from controllers import lib



class Inbox:
    def __init__(self, config):
        self.db_config = config
        self.table = "inbox"

    def getInfo (self, data):
        temp = { 
            'id' : data[0],
            'sender_number' : data[1],
            'sender_name' : data[2],
            'sender_id' : data[3],
            'sms_date' : data[4],
            'date_created' : lib.convertDate(data[5]),
            'message' : data[6],
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
