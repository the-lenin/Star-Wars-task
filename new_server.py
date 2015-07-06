#!/usr/bin/python
#encoding: utf-8

import sys
import socket
import MySQLdb
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

	conn.send('Menu:\n\n1)Registration\n\n2)Login\n\n')
	ans = conn.recv(1024)
	print ans

	if int(ans) == 1:
		conn.send('Enter your new nick: ')
		user_name = conn.recv(1024)
		conn.send('Enter your new password: ')
		user_pass = conn.recv(1024)
		res = Reg(user_name,user_pass)

	elif int(ans) == 2:
		conn.send('Enter your nick: ')
		user_name = conn.recv(1024)
		conn.send('Enter your password: ')
		user_pass = conn.recv(1024)
		res = Login(user_name,user_pass)

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

def Reg(name,passwd):
	result = cursor.execute("INSERT INTO base VALUES ('"+name+"','"+passwd+"');")
	if result == 1:
		return 'OK'

def Login(name_u,passwd1):
	data_s=cursor.execute("SELECT * FROM base WHERE name='"+name_u+"' and pass='"+passwd1+"';")
	print data_s
	if data_s == 1:
		return 'OK'



db=MySQLdb.connect(host="localhost", user="monty", passwd="some_pass", db="db1")
cursor = db.cursor()
while 1:
	conn, addr = sock.accept()
	print 'Connected with ' + addr[0] + ': ' + str(addr[1])
	
	start_new_thread(clientthread, (conn,addr))

s.close()