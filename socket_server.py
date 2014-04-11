from socket import *

__author__ = 'fanjunwei003'
HOST=''
PORT=21567
server_socket=socket(AF_INET,SOCK_STREAM)
server_socket.bind((HOST,PORT))
server_socket.listen(50)

while True:
    print 'wait connection'
    connection,address=server_socket.accept()
    print address

    data=connection.recv(1024)
    print  data
    connection.close()

server_socket.close()

