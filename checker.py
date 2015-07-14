import httplib2
import json
import os
import random
import string
import sys
import time
import socket
import re

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
def passwd_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# errors: (1,"sys.argv"),(2,"service unvailable"),(3,"Flag not found"),(4,"mumbled")

status = {
	"error" : [],
	"get" : 1,
	"put" : 1,
	"info" : "none",
}

def put_flag(ip, flag):
	user = id_generator()
	passwd = passwd_generator()	
	try:
		sock = socket.socket()                                                           
		sock.connect(('localhost', 8888))  
		a = sock.recv(10240)
		sock.send("1\n")
		a = sock.recv(10240)
		sock.send(user + "\n")
		a = sock.recv(10240)
		sock.send(passwd + "\n")
		a = sock.recv(10240)
		sock.send("3\n")
		sock.send(flag + "\n")
		a = sock.recv(10240)
		sock.close()

		if len(a) < 1:
			status["error"].append(4)
			return False

		return 1

	except:
		status["error"].append(4)
		return False

def check_flag(ip, user, passwd, flag):
	try:
		sock = socket.socket()                                                           
		sock.connect(('localhost', 8888))  
		a = sock.recv(10240)
		sock.send("2\n")
		a = sock.recv(10240)
		sock.send(user + "\n")
		a = sock.recv(10240)
		sock.send(passwd + "\n")
		a = sock.recv(10240)
	
		if "petushok" in a:
			status["error"].append(4)
			sock.close()
			return False

		a = sock.recv(10240)
		sock.send("4\n")
		a = sock.recv(10240)
		if flag in a:
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

if not len(sys.argv) == 6:
	print json.dumps(
		{
			"error" : [1,],
		}
	)
	sys.exit()

ip = sys.argv[1]
flag = sys.argv[2]
user = sys.argv[3]
passwd = sys.argv[4]
old_flag = sys.argv[5]

res1 = check_flag(ip, user, passwd, old_flag)
res2 = put_flag(ip,flag)

if res1 == False:
	status["get"] = 0
if res2 == False:
	status["put"] = 0
else:
	status["info"] = res2



print json.dumps(status)
