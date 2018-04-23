#!/usr/bin/python3

from socket import *
from time import ctime

HOST = '127.0.0.1'
PORT = '10086'
BUFSIZE = '1024'
ADDR = (HOST , PORT)

udp_client = socket(AF_INET , SOCK_DGRAM)

while True:
	data = raw_input('>>> ')
	if not data:
		break
	udp_client.sendto(data , ADDR)
	data , addr = udp_client.recvfrom(BUFSIZE)
	if not data:
		break
udp_client.close()