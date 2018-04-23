#!/usr/bin/python3

from socket import *
from time import ctime

HOST = '127.0.0.1'
PORT = 10086
BUFSIZE = '1024'
ADDR = (HOST , PORT)

udp_server = socket(AF_INET , SOCK_DGRAM)
udp_server.bind(ADDR)

while True:
	print('waiting for message...')
	data, addr = udp_server.recvfrom(BUFSIZE)
	udp_server.sendto( ('[%s] %s' %( ctime() , data)).ecode() )
	print(addr)

udp_server.close()
