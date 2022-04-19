import socket
import pickle
import sys
import select
from time import sleep
import fcntl, os
from MessageClass import Message
import security
from tkinter import *
class Client:
    def __init__(self, host='10.110.200.136', port=1233, buff=2048):
        self.host = host
        self.port = port
        self.buff = buff
        self.window = Tk()
        self.message_box = Entry(self.window, width=100, bg='white', fg='black')
        self.user_entry = Entry(self.window, width=20, bg='white', fg='black')
        self.output = Text(self.window, width=100, height=30, wrap=WORD, background='white')
        self.window.title('Hamza''s messaging')
        self.window.configure(background='black')
        Label(self.window, text='Enter Username: ', bg='black', fg='white', font='none 16 bold').grid(row=0, column=0, sticky=W)
        self.user_entry.grid(row=0, column=1, sticky=W)
        Button(self.window, text='Enter', width=5, command=self.get_user).grid(row=0, column=2, sticky=W)
        Label(self.window, text='MESSAGES', bg='black', fg='white', font='none 16 bold').grid(row=1, column=0, sticky=W)
        Label(self.window, text='ENTER MESSAGE:', bg = 'black', fg='white', font='none 16 bold').grid(row=2, column=0, sticky=W)
        self.message_box.grid(row=2, column=1, sticky=W)
        Button(self.window, text='Send', width=4, command=self.get_message).grid(row=2, column=2, sticky=W)
        self.output.grid(row=1, column=1, sticky=W)
        self.window.mainloop()

    def get_user(self):
        username = self.user_entry.get()
        return username

    def get_message(self):
        message = self.message_box.get()
        x = message
        self.output.insert(0, x)
        return message

    def start(self):
        with socket.socket() as sock:
            sock.connect((self.host, self.port))
            fcntl.fcntl(sock, fcntl.F_SETFL, os.O_NONBLOCK)
            print('Connected')
            username = self.user_entry.get
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
                    recv_user, recv_mess, enc_type, key, encrypted_image = serv_mess.unpack()
                    # if image_data:
                    #     cv2.imwrite(encrypted_image, image_data)
                    recv_mess = security.decode_random(enc_type=enc_type, secret_message=recv_mess, key=key, encrypted_image=encrypted_image)
                    # print( '\r' + recv_user + ': ' + recv_mess + ( ' ' * 50 ) + '\n' + 'Enter your message: ' , end = '' , flush = True )
                    self.output.insert(recv_mess)
                if self.message_box.get():
                    c = self.message_box.get()
                    if c:
                        if len( mess ) > 0:
                            mess_is_ready_to_send = True
                    else:
                        mess += c
                        sleep(.001)
                if mess_is_ready_to_send:
                    enc_type, secretmessage, key, encrypted_image = security.encode_random(mess)
                    mess_obj = Message(username, secretmessage, enc_type, key, encrypted_image)
                    out_mess = pickle.dumps(mess_obj)
                    sock.send(out_mess)
                    if mess == 'stop':
                        loop = False
                    mess = str()
                    mess_is_ready_to_send = False
                    # print('Enter your message: ' , end = '' , flush = True )
