from socket import *

HOST = '127.0.0.1'
PORT = 10086
ADDR = (HOST , PORT)
BUFSIZE = 1024

s = socket(AF_INET , SOCK_DGRAM)

s.bind(ADDR)

print('bind udp is 10086')

while True:
	data , addr = s.recvfrom(BUFSIZE)
	print('recv from %s:%s.' % addr)
	send_data = 'Hello %s' % data
	s.sendto(send_data.encode('utf-8') , addr)

