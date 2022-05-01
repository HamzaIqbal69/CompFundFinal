class HamzaIntroMessage:
    def __init__(self, enc_type, key):
        self.enc_type = enc_type
        self.key = key

    def unpackIntro(self):
        return self.enc_type, self.key
        