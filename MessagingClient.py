# import socket

# host = '127.0.0.1'
# port = 1233

# s = socket.socket()
# s.connect((host, port))
# clientmessage = bytes(str(input('Enter your message')) + '\n', 'utf-8')
# s.sendall(clientmessage)
# data = s.recv(1024)
# data = data.decode('utf-8')

# print(data)

import socket

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
while True:
    Input = input('Say Something: ')
    if Input == 'Stop':
        ClientSocket.send(str.encode(Input))
        break
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()
