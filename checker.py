import httplib2
import json
import os
import random
import string
import sys
import time
import socks
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
		socket = socks.socksocket()                                                           
		socket.connect((ip , 8888))  
		a = socket.recv(1024)
		socket.send("1\n")
		a = socket.recv(1024)
		socket.send(user + "\n")
		a = socket.recv(1024)
		socket.send(passwd + "\n")
		a = socket.recv(1024)
		socket.send("3\n")
		a = socket.recv(1024)
		socket.send(flag + "\n")
		a = socket.recv(1024)
		socket.close()

		if len(a) < 1:
			status["error"].append(4)
			return False

		return 1

	except:
		status["error"].append(4)
		return False

def check_flag(ip, user, passwd, flag):
	try:
		socket = socks.socksocket()                                                           
		socket.connect((ip , 8888))  
		a = socket.recv(1024)
		socket.send("2\n")
		a = socket.recv(1024)
		socket.send(user + "\n")
		a = socket.recv(1024)
		socket.send(passwd + "\n")
		a = socket.recv(1024)
	
		if "petushok" in a:
			status["error"].append(4)
			return False

		a = socket.recv(1024)
		socket.send("4\n")
		a = socket.recv(1024)
		if flag in a:
			return True
		else:
			status["error"].append(3)
			return False
	except:
		status["error"].append(4)
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
