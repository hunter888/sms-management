import humod
import requests
import time
import json
import unicodedata
from serial import SerialException
import mysql.connector
import serial
import re


URL_GETPORT = "http://127.0.0.1:8081/get_port"
URL_GETOUTBOX = "http://127.0.0.1:8081/get_outbox"
URL_DELETEOUTBOX = "http://127.0.0.1:8081/delete_outbox?id="
URL_ADDINBOX = "http://127.0.0.1:8081/addToInbox"
MODEM_FLAG = 0



# Open database connection
DB_CONFIG = {
  'user': 'smsadmin',
  'password': 'smsadmin',
  'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
  'database': 'sms',
  'raise_on_warnings': True,
}

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

def getInfo ( data):
    temp = { 
        'id' : data[0],
        'portname' : data[1],
        'status' : data[2],
        'network' : data[3],
        'balance' : data[4],
        'mobile_number' : data[5],
	'usb_id' : data[6],
        'model' : data[7],
        'isNotAvailable' : data[8],
        'lastUpdate' : data[9],
    }
    return temp

def update_usb_id (db_config, device_id, usb_id):
    query_string = "UPDATE modems SET usb_id='%s', status='Port ready for initialization',isNotAvailable=2 WHERE id=%d" % (str(usb_id), int(device_id))
    execDB (db_config, query_string)

def update_as_not_available (db_config, device_id, status):
    query_string = "UPDATE modems SET status='%s', isNotAvailable=1 WHERE id=%d" % (str(status), int(device_id))
    execDB (db_config, query_string)


def getModemDevices (db_config) :
    query_string = "SELECT * FROM modems" 
    db_data = queryDB(db_config, query_string)
       
    data_list = []
    for data in db_data:
        print data
        temp_data = getInfo(data)
        data_list.append(temp_data)
    return data_list


def getCurrentComPort ():
    r = requests.get(URL_GETPORT)
    return r.text


def addToMessageInbox(payload):
    r = requests.post(URL_ADDINBOX, data=payload)
    return r.text

def getOutboxMessages():
    r = requests.get(URL_GETOUTBOX)
    return json.loads(r.text)

def deleteOutbox (data_id):
    r = requests.get("%s%d" % (URL_DELETEOUTBOX, data_id) )
    return r.text
    

def initModem(comport):
    m = humod.Modem(comport, comport)
    try :
        model = m.show_model()
        if (model != None):
            MODEM_FLAG = 1
            print "Modem found"
            return m
        else:
            MODEM_FLAG = 0
            print model
            m.enable_textmode(True)
            print "No modem found"
    except SerialException:
        print "Cannot open com port"
    
    except Exception, e:
        print e
    except:
        print "theres an error"
        
    return None

def sendOutboxMessages (m, outbox):
    m.enable_textmode(True)
    for mess in outbox['outbox']:
    
        recipients = mess['recipients'].split(',')
        for rec in recipients:
            #try:
            if (1):
                print "sending %s to %s" % (mess['message'], rec)
                rec = rec.encode('ascii','ignore') 
                message =  mess['message'].encode('ascii','ignore')
                m.sms_send(rec, message)
                #m.sms_send(rec,"hi there")
                deleteOutbox(mess['id'])
            else:
            #except:
                print "send out error"
                m_humod.disconnect()
                return 0
    return 1


def checkInboxList (m):
    print "[checkInboxList]"
    m.enable_textmode(True)
    sms_list = m.sms_list()
    for sms in sms_list:
        print sms
	sms_id = sms[0]
	message = m.sms_read(sms_id)
	print message
	payload = { 'recipients' : sms[2],
		    'message' : message,
		    'timestamp' : sms[4]
		}
	addToMessageInbox(payload)
	m.sms_del(sms_id)

def main_bak():
    m_humod = None
    MODEM_FLAG = 0
    while(1):
        if (MODEM_FLAG):
            print "modem is ok"
            outbox = getOutboxMessages()
            if (outbox['count'] != 0):
                MODEM_FLAG = sendOutboxMessages (m_humod, outbox)
	    checkInboxList(m_humod)  
                
        else:
            print "modem not ok"
            comport = getCurrentComPort()
            print "Connecting modem via port %s" % comport
            m_humod = initModem(comport)
            if (m_humod == None):
                print "No modem found. trying again after 60s"
                time.sleep(60)
            else:
                MODEM_FLAG = 1
        time.sleep(15)


def isPortAvailable (device):
    retval = ""    
    print "start=========="
    #if True:
    try:
        print device['portname']
        s = serial.Serial(device['portname'])
        temp = "%s" % s
        print temp
        matchObj = re.search( "id=(.+?),", temp)
        usb_id =  matchObj.group(1)
        retval = usb_id
        s.close()
    #else:
    except serial.SerialException:
        print "serial.SerialException port unavailable"
        pass
    except ValueError:
	print "Cannot Configure port, access denied"
	pass
    return retval

def main(db_config):
    devices = getModemDevices(db_config)
    for device in devices:
        print device
        usb_id = isPortAvailable (device)
	if (usb_id == ""):
	    print "port is unavailable"
	    update_as_not_available(db_config, device['id'], "Port Unavailable")
	    continue
        print "usb_id :", usb_id
        update_usb_id (db_config, device['id'], usb_id)

    print "end"
    while True:
        print "watiting"
	time.sleep(5)
main(DB_CONFIG)

