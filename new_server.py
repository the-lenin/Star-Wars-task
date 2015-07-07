#!/usr/bin/python
#encoding: utf-8

import sys
import socket
import MySQLdb
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
	conn.send('It\'s our STAR WARS Service\n')
	conn.send("		    8888888888  888    88888\n                   88     88   88 88   88  88\n                    8888  88  88   88  88888\n                       88 88 888888888 88   88\n                88888888  88 88     88 88    888888\n\n                88  88  88   888    88888    888888\n                88  88  88  88 88   88  88  88\n                88 8888 88 88   88  88888    8888\n                 888  888 888888888 88   88     88\n                  88  88  88     88 88    8888888\n")
	conn.send('\nMenu:\n\n1)Registration\n\n2)Login\n\n')
	ans = conn.recv(1024)
	print ans

	if int(ans) == 1:
		conn.send('Enter your new dick: ')
		user_name = conn.recv(1024)
		user_name = user_name[0:(len(user_name)-2)]
		conn.send('Enter your new password: ')
		user_pass = conn.recv(1024)
		user_pass = user_pass[0:(len(user_pass)-2)]
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
		sock.close()
		exit

	else:
		conn.send('Sorry, you\'ve done something wrong.\n')
		sys.exit()

	if res == 'OK':
		Menu(user_name,user_pass)

	while True:
		data = conn.recv(1024)
		print 'Received data from ' + addr[0] + ': ' + str(addr[1])
		if not data:
			break
		
		conn.send(data) 

def Menu(name,passwd):
	print 'All is awesome!\n'
	sock.close()

def Reg(name,passwd):
	result = cursor.execute("INSERT INTO users VALUES ('"+name+"','"+passwd+"','ololol');")
	db.commit()
	print result
	if result == 1:
		return 'OK'

def Login(name_u,passwd1):
	data_s=cursor.execute("SELECT * FROM users WHERE name='"+name_u+"' and passwd='"+passwd1+"';")
	print data_s
	if data_s == 1:
		return 'OK'



db=MySQLdb.connect(host="localhost", user="monty", passwd="some_pass", db="db1")
cursor = db.cursor()
while 1:
	conn, addr = sock.accept()
	print 'Connected with ' + addr[0] + ': ' + str(addr[1])
	
	start_new_thread(clientthread, (conn,addr))


sock.close()
