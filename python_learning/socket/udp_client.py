from socket import *

s = socket(AF_INET , SOCK_DGRAM)

ADDR = ('127.0.0.1' , 10086)
#s.connect(('127.0.0.1' , 10086))

send_data = [b'lemon' , b'lisa' , b'bob']

for data in send_data:
	s.sendto(data , ADDR)
	print(s.recv(1024).decode('utf-8'))

s.close()