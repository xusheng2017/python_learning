#!/usr/bin/python3

from socket import *
from time import ctime

HOST = '127.0.0.1'
PORT = 10086
BUFSIZE = 1024
ADDR = (HOST , PORT)

while True:
	client_socket = socket(AF_INET , SOCK_STREAM)
	client_socket.connect(ADDR)
	data = input('>>> ')
	if not data:
		break
	client_socket.send( ('%s' % data).encode() )
	data = client_socket.recv(BUFSIZE)
	if not data:
		break
	print('data %s ' % data.strip())
	client_socket.close()