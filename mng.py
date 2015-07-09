#!/usr/bin/python
#encoding: utf-8
import os
import re
import sys
import json
import time
import socket
import pymongo
from pymongo import Connection
import string
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from thread import *


HOST = ''
PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	sock.bind((HOST, PORT))
except socket.error as msg:
	print 'Bind failed. Error: ' + str(msg[0]) + 'Message ' + msg[1]
	sys.exit()

sock.listen(10)

def clientthread(conn,addr):
	conn.send('	\t\tA long time ago in a galaxy far, far away...\n\n\n')
	time.sleep(3)
	os.system('clear')
	conn.send("		    8888888888  888    88888\n                   88     88   88 88   88  88\n                    8888  88  88   88  88888\n                       88 88 888888888 88   88\n                88888888  88 88     88 88    888888\n\n                88  88  88   888    88888    888888\n                88  88  88  88 88   88  88  88\n                88 8888 88 88   88  88888    8888\n                 888  888 888888888 88   88     88\n                  88  88  88     88 88    8888888\n")
	conn.send('\nMenu:\n\n1)Registration\n\n2)Login\n\n3)Get Your Side\n\n4)Show users\n\n')
	ans = conn.recv(1024)
	print ans

	if int(ans) == 1:
		conn.send('Enter your new dick: ')
		user_name = conn.recv(1024)
		user_name = user_name[0:(len(user_name)-2)]
		conn.send('Enter your new password: ')
		user_pass = conn.recv(1024)
		user_pass = user_pass[0:(len(user_pass)-2)]
		while res != 'OK':
			res = Reg(user_name,user_pass)

	elif int(ans) == 2:
		conn.send('Enter your dick: ')
		user_name = conn.recv(1024)
		user_name = user_name[0:(len(user_name)-2)]
		conn.send('Enter your password: ')
		user_pass = conn.recv(1024)
		user_pass = user_pass[0:(len(user_pass)-2)]
		res = Login(user_name,user_pass)
	
	elif int(ans) == 3:
		if res != 'OK':
			conn.send('You should log in\n')
		else:
			GetToken(user_name,user_pass)
	
	elif int(ans) == 4:
		table = db.users.find({}, {'name':1,'_id' : 0})
		for i in table:
			#res = re.findall('*\'name\' : u\'(*)\'*', i)
			print i
				
	else:
		conn.send('Sorry, you\'ve done something wrong.\n')
		sys.exit()

def Reg(name1,passwd1):
	n = db.users.find({'name':name1})
	#if n.count > 0:
	#	conn.send('User with this name already exists. Sorry, but IDI NAHUY')
	#else:
	db.users.insert( { 'name':name1, 'passwd':passwd1 } )
	return 'OK'
#первая уязвимость
#создавая пользователей с одинаковым именем мы сможем получать флаги всех пользователей с этим именем
def Login(name_u,passwd1):
	users = db.users.find({ 'name' : name_u, 'passwd' : passwd1 })
	if users.count != 0 :
		return 'OK'

def GetToken(name_u,passwd1):
	print db.users.find({'name' : name_u, 'passwd' : passwd1}, {'flag' : 1,'_id' : 0})
#вторая уязвимость
#лучше проверять _id, который создает mongo, иначе легко делать инъекцию
#а вообще нужно завести регулярку
	
while 1:
	conn, addr = sock.accept()
	connection =Connection()
	db = connection.db1
	print 'Connected with ' + addr[0] + ': ' + str(addr[1])
	
	start_new_thread(clientthread, (conn,addr))


sock.close()





