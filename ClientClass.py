import socket
import pickle
import sys
import select
from time import sleep
import fcntl, os
from MessageClass import Message
import security
import cv2
class Client:
    def __init__(self, host='10.110.200.136', port=1233, buff=2048):
        self.host = host
        self.port = port
        self.buff = buff
    def start(self):
        with socket.socket() as sock:
            sock.connect((self.host, self.port))
            fcntl.fcntl(sock, fcntl.F_SETFL, os.O_NONBLOCK)
            print('Connected')
            username = input('Enter username: ')
            loop = True
            mess = str()
            mess_is_ready_to_send = False
            print('Enter your message: ' , end = '' , flush = True )
            while loop:
                serv_mess = None
                try:
                    serv_mess = sock.recv(self.buff)
                except socket.error as e :
                    #err = e.args[ 0 ]
                    pass
                if serv_mess:
                    serv_mess = pickle.loads(serv_mess)
                    recv_user, recv_mess, enc_type, key, encrypted_image, image_data = serv_mess.unpack()
                    if image_data:
                        cv2.imwrite(encrypted_image, image_data)
                    recv_mess = security.decode_random(enc_type=enc_type, secret_message=recv_mess, key=key, encrypted_image=encrypted_image)
                    print( '\r' + recv_user + ': ' + recv_mess + ( ' ' * 50 ) + '\n' + 'Enter your message: ' , end = '' , flush = True )
                if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                    c = sys.stdin.read(1)
                    if c == '\n':
                        if len( mess ) > 0:
                            mess_is_ready_to_send = True
                    else:
                        mess += c
                        sleep(.001)
                if mess_is_ready_to_send:
                    enc_type, secretmessage, key, encrypted_image, image_data = security.encode_random(mess)
                    mess_obj = Message(username, secretmessage, enc_type, key, encrypted_image, img_data=image_data)
                    out_mess = pickle.dumps(mess_obj)
                    sock.send(out_mess)
                    if mess == 'stop':
                        loop = False
                    mess = str()
                    mess_is_ready_to_send = False
                    print('Enter your message: ' , end = '' , flush = True )

