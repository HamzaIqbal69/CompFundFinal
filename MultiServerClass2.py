import socket
import pickle
import threading
from MessageClass import Message
class multiServer:
    def __init__(self, host='10.110.200.136', port=1233, buff=2048):
        self.host = host
        self.port = port
        self.buff = buff
        self.connlst = []

    def start(self):
        with socket.socket() as s:
            s.bind((self.host, self.port))
            s.listen()
            print('listening')
            i = 0
            while True:
                conn, addr = s.accept()
                self.connlst.append(conn)
                print(f'Connected by {addr}')
                thread = threading.Thread(target=self.handle, args=(self.connlst[i],))
                thread.start()
                i += 1
                
    def handle(self, conn):
        #nwith conn:
            while True:
                raw_data = conn.recv(self.buff)
                if not raw_data:
                    break
                data = pickle.loads(raw_data)
                client_user, client_mess = data.unpack()
                print(f'Received {client_mess} from {client_user}')
                newData = Message(client_user, client_mess)
                newData = pickle.dumps(newData)
                #print(self.connlst)
                for i in self.connlst:
                    i.send(newData)
                print('Data sent')
            print(f'{client_user} disconnected')
            