import socket
#s = socket.socket()

def connectToServer(ip):
    host = ip
    port = 1234
    s.connect((host,port))

def sendPoint(s,point):
    """s = socket.socket()
    host = '192.168.1.3'
    port = 1234
    s.connect((host,port))"""
    s.send(point.encode('utf-8'))
    #rcv = s.recv(2048)

def disconnect(serverSocket):
    serverSocket.close()

def getMsg(s):
    return s.recv(2048)