# coding=utf-8
from socket import *

__author__ = 'fanjunwei003'
HOST='127.0.0.1'
PORT=21567
client_socket=socket(AF_INET,SOCK_STREAM)
client_socket.connect((HOST,PORT))
client_socket.send('测试我的链接')
client_socket.close()
