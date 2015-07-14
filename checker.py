import httplib2
import json
import random
import string
import time
import socket
import re
import os
import sys
import pymongo
import random
from pymongo import Connection
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from thread import *

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
def passwd_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
def flag_generator(size=32, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
# errors: (1,"sys.argv"),(2,"service unvailable"),(3,"Flag not found"),(4,"mumbled")

status = {
	"error" : [],
	"get" : 1,
	"put" : 1,
	"info" : "none",
}

def put_flag(i, ip):
	name1 = id_generator()
	passwd1 = passwd_generator()
	flag = flag_generator()
	db.users.insert({ 'name':name1, 'passwd':passwd1, '_id':i, 'flag': flag})
	try:
		sock = socket.socket()                                                           
		sock.connect((ip, 8888)) 
		print name1+'\n'
		print passwd1 + '\n'
		print flag + '\n'
		a = sock.recv(1024)
		print a
		time.sleep(1)
		sock.send("1")
		a = sock.recv(1024)
		print a
		time.sleep(1)
		sock.send(name1+'aa') #kogda vvodim ruchkami, my otbrasyvaem 2 simvola perevoda stroki,
		                      #a tut u nas golye siski - neprilichno
		a = sock.recv(1024)
		print a
		time.sleep(1)
		sock.send(passwd1+'aa')
		a = sock.recv(1024)
		print a
		time.sleep(1)
		sock.send("3")
		time.sleep(1)
		sock.send(flag+'aa')
		a = sock.recv(1024)
		print a
		time.sleep(1)
		sock.close()

		if len(a) < 1:
			status["error"].append(4)
			return False

		return 1

	except:
		status["error"].append(4)
		return False

def check_flag(i, ip):
	try:
		for i in db.users.find({'_id':i-1}):
			try:
				i['name']
				i['passwd']
				i['flag']
			except:
				print 'Sorry, but some shit has happened.'
			else:
				name = i['name']
				passwd = i['passwd']
				flag = i['flag']
		print name + ' abcd'
		print passwd + ' abcd'
		print flag + ' abcd'
		sock = socket.socket()                                                           
		sock.connect((ip, 8888))  
		a = sock.recv(1024)
		print a
		time.sleep(1)
		sock.send("2")
		a = sock.recv(1024)
		print a
		time.sleep(1)
		sock.send(name+'aa')
		a = sock.recv(1024)
		print a
		time.sleep(1)
		sock.send(passwd+'aa')
		a = sock.recv(1024)
		print a
		time.sleep(1)
	
		if "petushok" in a:
			status["error"].append(4)
			sock.close()
			return False

		a = sock.recv(1024)
		print a
		time.sleep(1)
		sock.send("4")
		a = sock.recv(1024)
		print a

		if flag in a:
			print 'Krasava!'
			sock.close()
			return True
		else:
			status["error"].append(3)
			sock.close()
			return False
	except:
		status["error"].append(4)
		sock.close()
		return False

def smack_my_bitch_up(i,ip):
	
	if i!=initial:
		res1 = check_flag(i, ip)
	res2 = put_flag(i, ip)

	if i!=initial:
		if res1 == False:
			status["get"] = 0
	if res2 == False:
		status["put"] = 0
	else:
		status["info"] = res2

	print json.dumps(status)

if not len(sys.argv) == 2:
	print json.dumps(
		{
			"error" : [1,],
		}
	)
	sys.exit()

time.sleep(4)
i=random.randint(1,10000000000000)
initial=i
ip=sys.argv[1]

connection =Connection()
db = connection.check
while True:
	status = {
	"error" : [],
	"get" : 1,
	"put" : 1,
	"info" : "none",
	}
	smack_my_bitch_up(i,ip)
	i+=1
	time.sleep(10)