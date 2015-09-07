import xmlrpclib
login = "0101010001"
password = "passwort"
server = "http://localhost:8022/app"
portal = xmlrpclib.Server(server)
print portal.checkAuth(login, password)
