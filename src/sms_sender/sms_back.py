import humod
import requests
import time
import json
import unicodedata
from serial import SerialException
from humod import siminfo
import mysql.connector
import serial
import re
import sys
import unicodedata
from GSM0338 import gsm0338_mapping



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
    }
    return temp


def getModemDevices (db_config) :
    query_string = "SELECT * FROM modems" 
    db_data = queryDB(db_config, query_string)
       
    data_list = []
    for data in db_data:
        print data
        temp_data = getInfo(data)
        data_list.append(temp_data)
    return data_list


def getTimeStamp():
    return time.strftime('%Y-%m-%d %H:%M:%S')
    
def convertDate (_date):
    if (_date == None):
        return " "
    return _date.strftime('%Y-%m-%d %H:%M:%S')


def getOutboxInfo ( data):
    temp = { 
        'id' : data[0],
        'outbox_since' : convertDate(data[1]),
        'mobile_number' : data[2],
        'recipient_name' : data[3],
        'priority' : data[4],
        'telco' : data[5],
        'message' : data[6],
        'status' : data[7],
        'date_sent' : convertDate(data[8]),
        'date_drafted' : convertDate(data[9]),
        'date_failed' : convertDate(data[10]),
    }
    return temp


def getOutbox (db_config) :
    query_string = "SELECT * FROM outbox WHERE status=0" 
    db_data = queryDB(db_config, query_string)
       
    data_list = []
    for data in db_data:
        print data
        temp_data = getOutboxInfo(data)
        data_list.append(temp_data)
    return data_list

			
def getdevice(db_config, _id):
    query_string = "SELECT * FROM modems WHERE id=%d" % (int(_id))
    db_data = queryDB(db_config, query_string)
    for data in db_data:
        return getInfo(data)

    return ""

def update_model (db_config, device, model):
    query_string = "UPDATE modems SET model='%s', status='Modem ready for sending sms' WHERE id=%d" % (str(model), int(device['id']))
    execDB (db_config, query_string)

def update_as_not_available (db_config, device, status):
    query_string = "UPDATE modems SET status='%s', isNotAvailable=1 WHERE id=%d" % (str(status), int(device['id']))
    execDB (db_config, query_string)


def initModem(db_config, device ):
    print "[initModem] portname %s" %  device['portname']
    m = humod.Modem(device['portname'], device['portname'])
    try :
        model = m.show_model()
        if (model != None):
            MODEM_FLAG = 1
            print "Modem found"
            update_model (db_config, device, model)
            return m
        else:
            MODEM_FLAG = 0
	    update_as_not_available (db_config, device, "Serial Port is not a modem")
            print "No modem found"
    except SerialException:
	update_as_not_available (db_config, device, "Cannot open Serial Port")
        print "Cannot open com port"
	pass
    
    except Exception, e:
        print e
	update_as_not_available (db_config, device, str(e))
	pass
    except:
        print "theres an error"
	update_as_not_available (db_config, device, "Device Error")
        
    return None

def splitMessageBy (split_count, message):
    split_message = []
    for i in range (0, split_count ):
	start = i * 105
	end = start + 105
	msg = message[start:end].strip()
	msg = "(%d of %d) %s" % (i+1, split_count, msg)
	split_message.append(str(msg))
    return split_message

def test ():
    message = "s you can see, they serve different purposes. The for loop runs for a fixed amount - in this case, 3, while the while loop theoretically runs forever. You could use a for loop with a huge number in order to gain the same effect as a while loop, but what's the point of doing that when you have a construct that already exists? As the old saying goes, why try to reinvent the wheel?"
    message_len = len(message)
    print "message_len", message_len
    if (message_len > 105 ):
        split_count = message_len / 105
	if (message_len % 105 > 0 ):
	    split_count += 1
	print "split_count" , split_count
        split_mess = splitMessageBy (split_count, message)
	print len(split_mess)
	print split_mess
	for mess in split_mess:
	    print len(mess)
	    print mess



def sendMessage( m_humod, recipient, message):

    message_len = len(message)
    m_humod.enable_textmode(True)
    rec = recipient.encode('ascii','ignore') 
    if (message_len > 105 ):
        split_count = message_len / 105
	if (message_len % 105 ):
	    split_count += 1

        split_mess = splitMessageBy (split_count, message)
	print len(split_mess)
	print split_mess
	for mess in split_mess:
	    print len(mess)
	    print mess
	    mess = str(mess)
            message =  mess.encode('ascii','ignore')
            m_humod.sms_send(rec, message)
	    time.sleep(1)



    else:
        message =  message.encode('ascii','ignore')
        m_humod.sms_send(rec, message)


def updateAsSent(db_config, outbox):
    ts = getTimeStamp()
    query_string = "UPDATE outbox SET date_sent='%s', status='2' WHERE id=%d" % (ts, int(outbox['id']))
    execDB (db_config, query_string)

def sendOutboxSMS (db_config, m_humod):
    data_list = getOutbox(db_config)
    for data in data_list:
        print data
        sendMessage( m_humod, data['mobile_number'], data['message'])
        updateAsSent(db_config, data)


def is_gsm_encoded(message):
    for x in message:
        if x not in '0123456789ABCDEF':
            return False
    return True

def decode_gsm(message):
    """ Tiny naive translation. For a proper codec try:
    https://github.com/dsch/gsm0338"""
    key = {a[2:]: chr(int(b, 0)) for a,b in gsm0338_mapping.items()}
    done = ''.join([key.get(x, '') for x in seq(message)])
    return done.replace('@', '')

def checkInboxList (db_config, m_humod):
    print "[checkInboxList]"
    m_humod.enable_textmode(True)
    #sms_list = m_humod.sms_list()
    sms_list = m_humod.full_sms_list("inbox")
    for sms in sms_list:
        print sms
	sms_id = sms[0]
	message = m_humod.sms_read(sms_id)
        
	print "message" , message
	gsm_encoded = is_gsm_encoded(message)
	if gsm_encoded :
	    print "gsm is encoded"
            message = decode_gsm(message)  if gsm_encoded else message
	print message
	payload = { 'recipients' : sms[2],
		    'message' : message,
		    'timestamp' : sms[4]
		}
	print payload
	#m_humod.sms_del(sms_id)


def runSenderOnPort (db_config, device_id):
    print "[runSenderOnPort] device_id %d " % device_id
    device =  getdevice(db_config, device_id)
    print device
    m_humod = initModem(db_config, device )
    if (m_humod == None):
        return

    while True:
        time.sleep(3)
        sendOutboxSMS (db_config, m_humod)
        checkInboxList (db_config, m_humod)
        





#test()
runSenderOnPort (DB_CONFIG, int(sys.argv[1]))















