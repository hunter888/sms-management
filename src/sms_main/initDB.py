import sqlite3 as lite
import sys

con = lite.connect('sms.db')

def createOutbox():
    cur.execute("CREATE TABLE OUTBOX(ID INTEGER PRIMARY KEY AUTOINCREMENT, \
        RECIPIENTS TEXT,     MESSAGE TEXT,   \
        TIMESTAMP TEXT,      STATUS TEXT   \
    )")

def createInbox():
    cur.execute("CREATE TABLE INBOX(ID INTEGER PRIMARY KEY AUTOINCREMENT, \
        RECIPIENTS TEXT,     MESSAGE TEXT,   \
        TIMESTAMP TEXT,      STATUS TEXT   \
    )")


def createSettings():
    cur.execute("CREATE TABLE SETTINGS(ID INTEGER PRIMARY KEY, \
        COM_PORT TEXT, \
        STATUS TEXT   \
    )")
    cur.execute("INSERT INTO SETTINGS VALUES(1,'COM4','ERROR')")
    con.commit()

with con:
    cur = con.cursor()
    createOutbox()
    createInbox()
    createSettings()



    
