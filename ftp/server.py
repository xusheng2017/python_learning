#! /usr/bin/python3  
# -*- coding: utf-8 -*-  
# client side  
  
import socket  
from threading import *  
import time  
  
  
def get_file():  
    data_socket_s = socket.socket()  
    data_socket_s.bind(('0.0.0.0', 8001))  
    data_socket_s.listen(1)  
    data_socket_c, data_socket_c_addr = data_socket_s.accept()   
    if data_socket_c:  
        print('get a server connection')  
        file_data = data_socket_c.recv(1024)  
        f = open('tmp', 'w')  
        f.write(file_data)  
        f.close()  
    data_socket_c.close()  
    data_socket_s.close()  
  
if __name__ == '__main__':  
    control_socket = socket.socket()  
    control_socket.connect(('127.0.0.1', 10086)) #根据需要更改地址  
    print('connected')  
    while True:  
        print('sending data')  
        in_data = raw_input('>>')  
        if in_data == 'q':  
            break;  
        if in_data == 'g': #开启接受文件线程  
            file_thread = Thread(target = get_file)  
            file_thread.start()  
            time.sleep(0.5)  
            control_socket.send('g')  
            file_thread.join()  
        else:  
            control_socket.send(in_data)  
  
    print('end')  
    control_socket.close() 