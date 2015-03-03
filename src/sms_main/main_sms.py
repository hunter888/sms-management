import sqlite3 as lite
from bottle import *
import bottle
import sys
import time
import json
import os
from controllers import users

STATIC_FILES = "/Users/mcandres/sandbox/CHRIS_BOTOR/sms_main/static"
BOWER_FILES = "/Users/mcandres/sandbox/CHRIS_BOTOR/sms_main/static/bower_components"


@route('/main/<filename:path>')
def server_static(filename):
    return static_file(filename, root=STATIC_FILES)

@route('/bower_components/<filename:path>')
def server_static(filename):
    return static_file(filename, root=BOWER_FILES)

bottle.route('/hello/<name>')(users.login)
bottle.route('/login', method='POST')(users.login)




run(host='localhost', port=8081, debug=True)
