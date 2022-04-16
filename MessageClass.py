class Message:
    def __init__(self, user, message, enc_type, key, enc_img, img_data):
        """
        Class for sending and receiving message objects
        """
        self.user = user
        self.message = message
        self.enc_type = enc_type
        self.key = key
        self.enc_img = enc_img
        self.img_data = img_data
    
    def unpack(self):
        return self.user, self.message, self.enc_type, self.key, self.enc_img, self.img_data
