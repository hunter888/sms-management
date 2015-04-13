from datetime import datetime
import time
import mysql.connector


def getTimeStamp():
    return time.strftime('%Y-%m-%d %H:%M:%S')
    
def convertDate (_date):
    if (_date == None):
        return " "
    return _date.strftime('%Y-%m-%d %H:%M:%S')

def queryDB (config, query_string):
    DB = mysql.connector.connect(**config)
    cursor = DB.cursor()
    cursor.execute(query_string)
    data_list = []
    for data in cursor:
        data_list.append(data)

    DB.close()
    return data_list

def execDB (config, query_string):
    DB = mysql.connector.connect(**config)
    cursor = DB.cursor()
    cursor.execute(query_string)
    DB.commit()
    DB.close()




