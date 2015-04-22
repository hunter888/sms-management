from bottle import template, request
import json
from controllers import lib
import urllib



class Outbox:
    def __init__(self, config):
        self.db_config = config
        self.table = "outbox"

    def getInfo (self, data):
        temp = { 
            'id' : data[0],
            'outbox_since' : lib.convertDate(data[1]),
            'mobile_number' : data[2],
            'recipient_name' : data[3],
            'priority' : data[4],
            'telco' : data[5],
            'message' : data[6] ,
            'status' : data[7],
            'date_sent' : lib.convertDate(data[8]),
            'date_drafted' : lib.convertDate(data[9]),
            'date_failed' : lib.convertDate(data[10]),
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


    def getWithStatus(self,status):
        query_string = "SELECT * FROM %s WHERE status=%s" % (self.table,str(status))
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

    def create(self):
        retval = {
            'success' : 'false'
        }
	print request.json['message']
        recipient_id = request.json["recipient_id"]
        priority = request.json["priority"]
        message = "%s" % str(request.json["message"])
        message = message.replace("'", "") 
        message = message.replace('"', "") 
	print "message", message

        query_string = "SELECT * FROM phonebook WHERE id=%s" % str(recipient_id)
        data_res = lib.queryDB(self.db_config, query_string)
        if ( len(data_res) > 0) :
            user_data = data_res[0]
            mobile_number =  user_data[3]
            recipient_name = user_data[2]
            telco = user_data[12]
            status = 0
            query_string = "INSERT INTO %s (mobile_number, recipient_name," % self.table
            query_string += " priority, telco, message, status) VALUES "
            query_string += "('%s', '%s','%s','%s','%s',%d)" % (mobile_number, recipient_name, priority,telco,message, status)
	    print "query_string", query_string
            lib.execDB(self.db_config, query_string)

            retval = {
                'success' : 'true'
            }

        return retval













