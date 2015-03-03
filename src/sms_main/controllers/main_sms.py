import sqlite3 as lite
from bottle import route, run, template, request, static_file
import sys
import time
import json
import os

DB_CON = lite.connect('sms.db')
STATIC_FILES = "/Users/mcandres/sandbox/CHRIS_BOTOR/sms_main/static"


@route('/<filename:path>')
def server_static(filename):
    return static_file(filename, root=STATIC_FILES)



## DATABASE METHODS
def addToMessage (tablename, recipients, message, timestamp, status):
    max_id = getMaxId(tablename)
    sql_string =  "INSERT INTO %s VALUES(%d,'%s','%s','%s','%s') " % (tablename, max_id, recipients, message, timestamp, status)
    print sql_string
    cur = DB_CON.cursor()
    cur.execute(sql_string)
    DB_CON.commit()

def updateComPort (com_port):
    sql_string =  "UPDATE SETTINGS SET COM_PORT='%s' WHERE ID=1" % com_port
    print sql_string
    cur = DB_CON.cursor()
    cur.execute(sql_string)
    DB_CON.commit()


def updateComStatus (com_status):
    sql_string =  "UPDATE SETTINGS SET STATUS='%s' WHERE ID=1" % com_status
    print sql_string
    cur = DB_CON.cursor()
    cur.execute(sql_string)
    DB_CON.commit()


def deleteFromTable(table_name, data_id):
    sql_string =  "DELETE FROM %s WHERE ID=%d" % (table_name, data_id)
    print sql_string
    cur = DB_CON.cursor()
    cur.execute(sql_string)
    DB_CON.commit()

    

def getDataFromTable (tablename):
    cur = DB_CON.cursor()
    sql_string = "SELECT * FROM %s ORDER BY ID DESC" % tablename
    cur.execute(sql_string)
    rows = cur.fetchall()
    return rows

def getMaxId (tablename):
    cur = DB_CON.cursor()
    sql_string = "SELECT MAX(ID) FROM %s" % tablename
    cur.execute(sql_string)
    row = cur.fetchone()
    if (row[0] == None):
        return 1
    else:
        return row[0] + 1





def getCurrentDateTime():
    return time.strftime("%c")
    


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


@route('/create_message', method='POST')
def create_message():
    recipients = request.forms.get('recipients')
    message = request.forms.get('message')
    timestamp = getCurrentDateTime()
    addToMessage ("OUTBOX", recipients, message, timestamp , "On Queue")
    stat_mess ="Your message to %s has been sent to the queue" % recipients
    return template('template\create.tpl', stat=stat_mess)




def openFileAndAddToOutbox (savepath, message_def):
    data = []
    with open(savepath, 'r') as open_file:
        for line in open_file.readlines():
	    print line
	    split_line = line.split(',')
	    recipient = split_line[0].strip()
	    message = split_line[1].strip()
	    print "*", message , "*"
	    if (message == ''):
                message = message_def
	    print "recipient:", recipient , " message:", message
            timestamp = getCurrentDateTime()
            addToMessage ("OUTBOX", recipient, message, timestamp , "On Queue")
	    temp = [ recipient,message]
	    data.append(temp)

    return data


@route('/create_bulk_message', method='POST')
def create_bulk_message():
    upload = request.files.get("upload")
    message = request.forms.get("message")
    stat_mess = "Data is now queued in the system"
    data = []
    if upload is not None:
        name, ext = os.path.splitext(upload.filename)

        if ext not in ('.csv','.txt'):
            stat_mess = "File extension not allowed. must be txt or csv"
            return template('template\\bulk.tpl', stat=stat_mess, data=data)
        category = "csv"

        save_path = "upload/".format(category=category)
        if not os.path.exists(save_path):
            print "path does not exists"
            os.makedirs(save_path)

        file_path = "{path}/{file}".format(path=save_path, file=upload.filename)

        with open(file_path, 'wb') as open_file:
            open_file.write(upload.file.read())
            open_file.close()
	data = openFileAndAddToOutbox(file_path, message)


    else: 
        print "upload is None Type"




    message = request.forms.get('message')
    timestamp = getCurrentDateTime()
    return template('template\\bulk.tpl', stat=stat_mess, data=data)




@route('/addToInbox', method='POST')
def addToInbox():
    recipients = request.forms.get('recipients')
    message = request.forms.get('message')
    timestamp = request.forms.get('timestamp')
    addToMessage ("INBOX", recipients, message, timestamp, "Unread" )
    return "OK"


@route('/change_settings', method='POST')
def change_settings():
    com_port = request.forms.get('com_port')
    updateComPort(com_port)

    rows = getDataFromTable ('SETTINGS')
    com_port = rows[0][1]
    com_status = rows[0][2]
    return template('template/settings.tpl', com_port=com_port, com_status=com_status, table_name='SETTINGS', stat=' ')



@route('/update_com_status', method='POST')
def update_com_status():
    com_status = request.forms.get('com_status')
    updateComStatus(com_status)
    return "OK"

@route('/delete_outbox')
def delete_outbox():
    data_id = request.query.id
    deleteFromTable("OUTBOX", int(data_id))
    return "ok"

@route('/get_port')
def get_port():
    rows = getDataFromTable("SETTINGS")
    com_port = rows[0][1]
    return "%s" % com_port

@route('/get_outbox')
def get_outbox():
    rows = getDataFromTable("OUTBOX")
    data = {}
    data['outbox'] = []
    for row in rows:
	mess = {
 	    "id" : row[0],
	    "recipients" : row[1],
	    "message" : row[2]
	}
	data['outbox'].append(mess)


    data['count'] = len(rows)
    return json.dumps(data)




@route('/create')
def create():
    return template('template/create.tpl', stat=' ')


@route('/bulk')
def bulk():
    data = []
    return template('template/bulk.tpl', stat=' ', data=data)

@route('/outbox')
def outbox():
    rows = getDataFromTable ('OUTBOX')
    return template('template/messages.tpl', rows=rows, table_name='OUTBOX', stat=' ', delete_string="delete_outbox")


@route('/inbox')
def inbox():
    rows = getDataFromTable ('INBOX')
    return template('template/messages.tpl', rows=rows, table_name='INBOX', stat=' ',  delete_string="delete_inbox")



@route('/delete_inbox')
def delete_inbox():
    data_id = request.query.id
    deleteFromTable("INBOX", int(data_id))
    rows = getDataFromTable ('INBOX')
    return template('template/messages.tpl', rows=rows, table_name='INBOX', stat=' ', delete_string='delete_inbox')



@route('/delete_outbox')
def delete_outbox():
    data_id = request.query.id
    deleteFromTable("OUTBOX", int(data_id))
    rows = getDataFromTable ('OUTBOX')
    return template('template/messages.tpl', rows=rows, table_name='OUTBOX', stat=' ',delete_string='delete_outbox')



@route('/settings')
def settings():
    rows = getDataFromTable ('SETTINGS')
    com_port = rows[0][1]
    com_status = rows[0][2]
    return template('template/settings.tpl', com_port=com_port, com_status=com_status, table_name='SETTINGS', stat=' ')



run(host='localhost', port=8081, debug=True)
