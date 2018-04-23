#!/usr/bin/python3
#coding=utf-8
from socket import *
from time import ctime

HOST = ''
PORT = 8000
BUFSIZE = 1024
ADDR = (HOST , PORT)

m_server = socket(AF_INET , SOCK_STREAM)
m_server.bind(ADDR)
m_server.listen(5)

while True:
	print('waiting for connection ...')
	m_client , addr = m_server.accept()
	print('...connected from :' , addr)
	while True:
		data = m_client.recv(BUFSIZE).decode()
		print(data)
		if not data:
			break
		m_client.send( ('[%s] %s' % ( ctime() , data ) ).encode() ) 
	m_client.close()
m_server.close()
