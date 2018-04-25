#!/usr/bin/python3

from socketserver import (TCPServer as TCP , StreamRequestHandler as SRH )
from time import ctime


HOST = '127.0.0.1'
PORT = 10086
BUFSIZE = 1024
ADDR = (HOST , PORT)

class MyRequestHandle(SRH):
	def handle(self):
		print('...connect from:' , self.client_address)
		print(self.rfile.readline().decode())
		#  self.wfile.write(self.rfile.readline())
		self.wfile.write( ('[%s] %s' % (ctime() , self.rfile.readline()) ).decode())


tcp_server = TCP(ADDR , MyRequestHandle)
print('waiting for connection...')
tcp_server.serve_forever()