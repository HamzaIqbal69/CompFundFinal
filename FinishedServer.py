###############################################################################
# This is the Server that allows the messaging app to work, it receives       #
# messages from either client and decodes them, then re encodes the messages  #
# and broadcasts them to all the connected clients.  The server uses          #
# multithreading in order to provide functionality to multiple clients        #
# simultaneously.  A class was used for the server rather than simply running #
# it in a main program to make the program easier to troubleshoot and         #
# debug.                                                                      #
###############################################################################

# Imports ---------------------------------------------------------------------

import socket
import pickle
import threading
from FinishedMessageClass import HamzaMessage
import FinishedSecurity

# Class Declaration -----------------------------------------------------------

class multiServer:

    # Function Definitions ----------------------------------------------------

    def __init__(self, host='10.110.200.136', port=1234, buff=2048):
        """
        This function initializes the multiServer object and sets default
        values for the host ip address, port number, and buffer size all
        of which are necessary when working with sockets.  Additionally 
        defines an empty list, which will be filled with the different
        connections to help keep track of the connections and send messages
        back and forth to all the connections.
        """
        self.host = host
        self.port = port
        self.buff = buff
        self.connlst = []

    def start(self):
        """
        This function starts and maintains the server, and is responsible 
        for managing the connections.  When a new user connects a new thread
        is opened and that connection is added to the list of connections.
        """
        with socket.socket() as s:
            # Setting up the socket -------------------------------------------
            s.bind((self.host, self.port))
            s.listen()
            print('listening')
            i = 0
            # Infinite loop for accepting new connections ---------------------
            while True:
                conn, addr = s.accept()
                self.connlst.append(conn)
                print(f'Connected by {addr}')
                # Starting a new thread and having the handle function take care
                # of the connection --------------------------------------------
                thread = threading.Thread(target=self.handle, args=(self.connlst[i],))
                thread.start()
                i += 1
                
    def handle(self, conn):
        """
        This is the function that accepts messages from the clients,
        decodes them, re encodes them and then broadcasts the message
        to all the clients.
        """
        client_user = ''
        # Loop to keep accepting messages from the socket and then 
        # broadcasting them to the rest of the clients -------------------------
        while True:
            # If a message is not received the loop breaks and connection terminates
            raw_data = conn.recv(self.buff)
            if not raw_data:
                break
            # If a message is received then the message is decoded here, then re
            # encoded, and then sent to all the connections in the list of connections
            data = pickle.loads(raw_data)
            client_user, client_mess, enc_type, key = data.unpack()
            client_mess = FinishedSecurity.decode_random(enc_type=enc_type, secret_message=client_mess, key=key)
            print(f'Received {client_mess} from {client_user}')
            enc_type, client_mess, key = FinishedSecurity.encode_random(client_mess)
            newData = HamzaMessage(client_user, client_mess, enc_type, key)
            newData = pickle.dumps(newData)
            for i in self.connlst:
                i.send(newData)
            print('Data sent')
        print(f'{client_user} disconnected')
            