import MySQLdb
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler


db=MySQLdb.connect(host="localhost", user="monty", passwd="some_pass", db="db1")
cursor = db.cursor()
name_u=raw_input("Enter username")
passwd1=raw_input("Enter password")
data_s=cursor.execute("SELECT * FROM users WHERE name='"+name_u+"' and passwd='"+passwd1+"';")

print data_s
print "		    8888888888  888    88888\n                   88     88   88 88   88  88\n                    8888  88  88   88  88888\n                       88 88 888888888 88   88\n                88888888  88 88     88 88    888888\n\n                88  88  88   888    88888    888888\n                88  88  88  88 88   88  88  88\n                88 8888 88 88   88  88888    8888\n                 888  888 888888888 88   88     88\n                  88  88  88     88 88    8888888"


# WHERE passwd == passwd1
