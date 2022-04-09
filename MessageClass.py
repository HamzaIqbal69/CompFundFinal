class Message:
    def __init__(self, user, message):
        """
        Class for sending and receiving message objects
        """
        self.user = user
        self.message = message
    
    def unpack(self):
        return self.user, self.message
