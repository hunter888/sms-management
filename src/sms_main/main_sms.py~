import sqlite3 as lite
from bottle import *
import bottle
import sys
import time
import json
import os
from controllers import users
from controllers import inbox
from controllers import outbox
from controllers import phonebook
from controllers import serialport
import mysql.connector


# Open database connection
config = {
  'user': 'smsadmin',
  'password': 'smsadmin',
  'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
  'database': 'sms',
  'raise_on_warnings': True,
}


STATIC_FILES = "static"
BOWER_FILES = "static/bower_components"

# instantiate user controllers
UserCtrl = users.Users(config)
InboxCtrl = inbox.Inbox(config)
OutboxCtrl = outbox.Outbox(config)
PhoneBookCtrl = phonebook.PhoneBook(config)
SerialCtrl = serialport.SerialPort(config)

@route('/main/<filename:path>')
def server_static(filename):
    return static_file(filename, root=STATIC_FILES)

@route('/bower_components/<filename:path>')
def server_static(filename):
    return static_file(filename, root=BOWER_FILES)

bottle.route('/hello/<name>')(UserCtrl.login)
bottle.route('/login', method='POST')(UserCtrl.login)
bottle.route('/users/create', method='POST')(UserCtrl.create)
bottle.route('/users/all')(UserCtrl.all)
bottle.route('/users/get/<user_id>')(UserCtrl.get)

bottle.route('/inbox/all')(InboxCtrl.all)
bottle.route('/inbox/get/<_id>')(InboxCtrl.get)
bottle.route('/inbox/delete/<_id>')(InboxCtrl.delete)

bottle.route('/outbox/all')(OutboxCtrl.all)
bottle.route('/outbox/get/<_id>')(OutboxCtrl.get)
bottle.route('/outbox/delete/<_id>')(OutboxCtrl.delete)
bottle.route('/outbox/getWithStatus/<status>')(OutboxCtrl.getWithStatus)
bottle.route('/outbox/create', method='POST')(OutboxCtrl.create)

bottle.route('/phonebook/all')(PhoneBookCtrl.all)
bottle.route('/phonebook/get/<_id>')(PhoneBookCtrl.get)
bottle.route('/phonebook/delete/<_id>')(PhoneBookCtrl.delete)
bottle.route('/phonebook/create', method='POST')(PhoneBookCtrl.create)

bottle.route('/serial/getAllDevices')(SerialCtrl.getAllDevices)
bottle.route('/serial/all')(SerialCtrl.all)
bottle.route('/serial/delete/<_id>')(SerialCtrl.delete)
bottle.route('/serial/get/<_id>')(SerialCtrl.get)
bottle.route('/serial/addAsModem',method='POST')(SerialCtrl.addAsModem)

run(host='0.0.0.0', port=8081, debug=True)
