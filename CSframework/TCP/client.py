#!/usr/bin/python3
#coding=utf-8

from socket import *
from time import ctime

HOST = '127.0.0.1'
PORT = 8000
BUFSIZE = 1024
ADDR = (HOST , PORT)


m_client = socket(AF_INET , SOCK_STREAM)
m_client.connect(ADDR)

while True:
	data = input('>>> ')
	if not data:
		break
	m_client.send(data.encode())
	data = m_client.recv(BUFSIZE).decode()
	if not data:
		break
	print(data)
m_client.close()

