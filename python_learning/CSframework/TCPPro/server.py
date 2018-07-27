#!/usr/bin/python3
#coding = utf-8

from socket import *
from time import ctime
from time import localtime
import time

HOST = '127.0.0.1'
PORT = 10086
BUFSIZE = 1024
ADDR = (HOST , PORT)

m_server = socket(AF_INET , SOCK_STREAM)
m_server.bind(ADDR)
m_server.listen(5)

STOP_CHAT = False

while not STOP_CHAT:
	print('listen port:%s' % (PORT))
	m_client , addr = m_server.accept()
	print('received addr:%s'  , addr)
	while True:
		try:
	   		data = m_client.recv(BUFSIZE)
		except:
			m_client.close()
			break
		if not data:
			break
		ISOTIMEFORMAT = '%Y-%m-%d %X'
		stime = time.strftime(ISOTIMEFORMAT , localtime())
		s = 'client %s send is:%s' % (addr[0] , data.decode('utf-8'))
		m_client.send(s.encode('utf-8'))
		print([stime] , ':' , data.decode('utf-8'))
		STOP_CHAT = (data.decode('utf-8').upper()=="QUIT")
		if STOP_CHAT:
#			break
			
m_client.close()
m_server.close()




