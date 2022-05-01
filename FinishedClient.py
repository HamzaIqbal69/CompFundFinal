############################################################################################
# The purpose of this program is to provide the client of the client server messaging      #
# architecture.  This client program incorporates a Graphical User Interface to make the   #
# application more appealing to the user.  The client opens up a GUI window and from there #
# the user can input username information, see messages, and input their own messages.     #
# The client program takes the inputted messages and sends them to the server program via  #
# TCP sockets, so that the message can be broadcasted to the rest of the users.            #
############################################################################################

# Imports ----------------------------------------------------------------------------------

import socket
import pickle
import fcntl, os
from FinishedMessageClass import HamzaMessage
import FinishedSecurity
from tkinter import *

# Class Declaration ------------------------------------------------------------------------

class Client:

    # Function Definitions -----------------------------------------------------------------

    def __init__(self, host='0.0.0.0', port=1234, buff=2048):
        """
        This function initializes all the variables we will need in the rest of our functions
        """
        self.host = host
        self.port = port
        self.buff = buff
        self.username = str()
        self.message = None
        self.window = None
        self.message_box = None
        self.user_entry = None
        self.output = None
        self.mess_is_ready_to_send = False
        self.sock = None

    def get_user(self):
        """
        This function enables the username submission button in the GUI and passes the value
        from the GUI entry box to the username that will be used to send messages to the server
        """
        self.username = str(self.user_entry.get())
        
    def get_message(self):
        """
        Gets the user message from the message entry box.  This function is enabled by the 
        Send button in the GUI, and the value that this function assigns to self.message 
        will be used as the body of the message sent by the client to the server.
        """
        message = self.message_box.get()
        self.message = str(message)

    def refresh(self):
        """
        Refreshes the GUI so that new messages can be showcased. 
        Also calls the task function, which actually sends messages to the server.
        """
        self.window.update()
        self.window.after(500, self.refresh)
        self.task()
        
    def task(self):
        """
        This function handles the actual receiving and sending of messages over TCP 
        sockets.  If a message is received then it will decode and display the message
        in the GUI, and if a message is entered using the Send button then that message
        is encoded and sent to the server.
        """
        # Handling the case where a message is received from the server --------------------
        serv_mess = None
        try:
            serv_mess = self.sock.recv(self.buff)
        except socket.error as e :
            pass
        if serv_mess:
            serv_mess = pickle.loads(serv_mess)
            recv_user, recv_mess, enc_type, key = serv_mess.unpack()
            for i in range(5):
                enc_type = FinishedSecurity.decode_custom(enc_type)
            recv_mess = FinishedSecurity.decode_random(enc_type=enc_type, secret_message=recv_mess, key=key)
            self.output.insert(END, f'{recv_user}:  {recv_mess} \n')
        # Handling the case where a message is entered into the text box -------------------
        if self.message:
            self.mess_is_ready_to_send = True
        if self.mess_is_ready_to_send is True:
            messboi = self.message
            user = self.username
            enc_type, secretmessage, key = FinishedSecurity.encode_random(messboi)
            for i in range(5):
                enc_type = FinishedSecurity.encode_custom(enc_type)
            mess_obj = HamzaMessage(user, secretmessage, enc_type, key)
            out_mess = pickle.dumps(mess_obj)
            self.sock.send(out_mess)
            self.message = None
            self.mess_is_ready_to_send = False
        
    def runClient(self):
        """
        This function connects the socket, sets up the GUI.
        It also calls the refresh function, which updates the GUI and 
        runs the task function, which is what gives this class its functionality.
        This is the only function that needs to be called to run the client.
        """
        # Setting up the socket -------------------------------------------------------------
        with socket.socket() as self.sock:
            self.sock.connect((self.host, self.port))
            fcntl.fcntl(self.sock, fcntl.F_SETFL, os.O_NONBLOCK)
            print('Connected')
            # GUI Setup ----------------------------------------------------------------------
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
            self.output.insert(1.0, 'MESSAGES DISPLAYED BELOW\n\n')
            # Calling refresh to actually make the program functional --------------------------
            self.refresh()    
            self.window.mainloop()