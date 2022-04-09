#########################################################
# NEEDS:                                                #
#   Open 2 connections to 2 clients                     #
#   Get message from whichever client sends stuff first #
#   Send that message to the other client               #
#   Repeat Until either client terminates               #
# IMPORTANT CASES:                                      #
#   If a client sends a message and the other client is #
#   not active, must send an error message to sending   #
#   client that message cannot be sent                  #
#########################################################

import socket
import os
from _thread import *

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection):
    
    connection.send(str.encode('Welcome to the Servern'))
    while True:
        data = connection.recv(2048)
        reply = 'Server Says: ' + data.decode('utf-8')
        if data.decode('utf-8') == 'Stop':
            break
        connection.sendall(str.encode(reply))
    connection.close()
    return False


while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()







# import socket
# host = '127.0.0.1' # localhost
# port = 65433

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((host, port))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print(f'Connected by {addr}')
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             print('kachow i got them data bois')
#             print('here is what i got')
#             data = data.decode('utf-8')
#             print(data)
#             newData = data.split(' ')
#             for i in range(len(newData)):
#                 if newData[i] == 'client':
#                     newData[i] = 'server'
#             newData = ' '.join(newData)
#             servermessage = bytes(newData, 'utf-8')
#             conn.sendall(servermessage)
#             print('kachow i sent them daters')
