#! /usr/bin/python3  
# -*- coding: utf-8 -*-  
# server side  
  
from socket import *  
  
if __name__ == '__main__':  
    s_listen_socket = socket()  
    s_listen_socket.bind(('0.0.0.0', 8000))  
    print('b4 listening')  
    s_listen_socket.listen(2)  
      
    control_socket, client_addr  = s_listen_socket.accept()  
#    control_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  
    print client_addr[0]  
    print('incoming connection')  
    if control_socket:   
        while True:  
            recv_data = control_socket.recv(20)  
            if not recv_data:  
                break;  
            print('control receiving %s' % recv_data)  
            if recv_data == 'g':  
                print('sending file tmp')  
                data_socket = socket()  
#                data_socket.bind(('127.0.0.2', 8001))  
                data_socket.connect((client_addr[0], 8001))  
                out_file = open('tmp', 'r')  
                send_data = out_file.read()  
                data_socket.send(send_data)  
                out_file.close()  
                data_socket.close()  
                recv_data = ''  
                print('sending file tmp done')  
            else:  
                print('receiving %s' % recv_data)  
                control_socket.send(recv_data)  
    print('end')  
    s_listen_socket.close()  
    control_socket.close()  
