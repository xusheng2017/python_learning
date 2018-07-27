from socket import *
'''
s = socket(AF_INET , SOCK_STREAM )

s.connect(('www.sina.com.cn' , 80))

send_data = 'GET / HTTP/1.1\r\nHost:www.sina.com.cn\r\nConnecttion:close\r\n\r\n'.encode('utf-8')
print(send_data)
recv_data = []

s.send(send_data)

while True:
	d = s.recv(1024)
	if d:
		recv_data.append(d)
		#print(recv_data)
	else:
		break

data = b''.join(recv_data)

s.close()

header , html = data.split(b'\r\n\r\n' ,1)
print(header.decode('utf-8'))

with open('sina.html' , 'wb') as f:
	f.write(html)

'''

s = socket(AF_INET , SOCK_STREAM)
print(s)
s.connect(('127.0.0.1' , 10086))
print(s.recv(2014).decode('utf-8'))

send_data = [b'lemon' , b'bob' , b'lisa']

for data in send_data:
	s.send(data)
	print(s.recv(1024).decode('utf-8'))

s.send(b'exit')
s.close()