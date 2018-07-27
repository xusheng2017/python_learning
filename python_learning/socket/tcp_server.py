from socket import *
import threading
import time

HOST = '127.0.0.1'
PORT = 10086
BUFSIZE = 1024
ADDR = (HOST , PORT)

s = socket(AF_INET , SOCK_STREAM)

s.bind(ADDR)

s.listen(5)
print('waiting for connection...')

def tcplink(sock , addr):
	print(sock)
	print('accept new connection from %s:%s ' % addr)
	sock.send(b'Welcome')
	while True:
		data = sock.recv(BUFSIZE)
		time.sleep(1)
		if not data or data.decode('utf-8') == 'exit':
			break
		sock.send(('Hello, %s' % data.decode('utf-8')).encode('utf-8'))
	sock.close()
	print('connection from %s:%s closed' % addr )

while True:
	sock , addr = s.accept()
	t = threading.Thread(target = tcplink , args = (sock , addr))
	t.start()



