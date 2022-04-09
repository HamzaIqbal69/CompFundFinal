import socket
import pickle
from MessageClass import Message
class Server:
    def __init__(self, host='127.0.0.4', port=1234, buff=2048):
        self.host = host
        self.port = port
        self.buff = buff
    def start(self):
        with socket.socket() as s:
            s.bind((self.host, self.port))
            s.listen()
            print('listening')
            conn, addr = s.accept()
            with conn:
                print(f'Connected by {addr}')
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    data = pickle.loads(data)
                    client_user, client_mess = data.unpack()
                    print(f'Received {client_mess} from {client_user}')
                    newData = Message('server', client_mess[::-1])
                    newData = pickle.dumps(newData)
                    conn.sendall(newData)
                    print('Data sent')