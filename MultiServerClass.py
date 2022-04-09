import socket
import pickle
import threading
from MessageClass import Message
class multiServer:
    def __init__(self, host='127.0.0.1', port=65433, buff=2048):
        self.host = host
        self.port = port
        self.buff = buff

    def start(self):
        with socket.socket() as s:
            s.bind((self.host, self.port))
            s.listen()
            print('listening')
            while True:
                conn, addr = s.accept()
                print(f'Connected by {addr}')
                thread = threading.Thread(target=self.handle, args=(conn,))
                thread.start()
                
    def handle(self, conn):
        with conn:
            while True:
                raw_data = conn.recv(self.buff)
                if not raw_data:
                    break
                data = pickle.loads(raw_data)
                client_user, client_mess = data.unpack()
                print(f'Received {client_mess} from {client_user}')
                newData = Message('server', client_mess[::-1])
                newData = pickle.dumps(newData)
                conn.sendall(newData)
                print('Data sent')
            print(f'{client_user} disconnected')
            