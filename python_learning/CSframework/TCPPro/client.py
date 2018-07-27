#!/usr/bin/python3
#coding = 'utf-8'

from socket import *
from time import ctime
from time import localtime
import time

class m_client:
	HOST = '127.0.0.1'
	PORT = 10086
	BUFSIZE =1024
	ADDR = (HOST , PORT)
	def __init__(self):
		self.client=socket(AF_INET , SOCK_STREAM)
		self.client.connect(self.ADDR)

		while True:
			data = input('>>>')
			if not data:
				break
			self.client.send(data.encode('utf-8'))
			print('client send message to %s:%s' % (self.HOST , data) )
			if data.upper()=='QUIT':
				break
			data = self.client.recv(self.BUFSIZE)
			if not data:
				break
			print('from %s recv:%s' % (self.HOST , data.decode('utf-8') ) )



if __name__ == '__main__':
	client=m_client()
