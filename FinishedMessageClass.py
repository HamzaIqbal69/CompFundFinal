###############################################################
# Created a message object to be able to succinctly hold all  #
# the data that the clients and server need to be able to     #
# decode and encode all the messages, along with user name    #
# information.                                                #
###############################################################

# Class Declaration ------------------------------------------- 

class HamzaMessage:

# Function Definitions ----------------------------------------

    def __init__(self, user, message):
        """
        Class for sending and receiving message objects
        The information held in this object is the client's
        username, the message, the type of encoding used on the 
        message, and if needed the key to decode the message.
        """
        self.user = user
        self.message = message
         
    def unpack(self):
        """
        Returns all the different object parameters, specified
        in the above function.
        """
        return self.user, self.message
