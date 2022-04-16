from numpy import rec
import rsa
import security
import cv2


message = 'Hello im all encrpted so cool'
enc_type, secretmessage, key, encrypted_image = security.encode_random(message)
print(f'Encoding Type: {enc_type}\nMessage: {secretmessage}\nKey: {key}\nImage: {encrypted_image}')
received = security.decode_random(enc_type=enc_type, secret_message=secretmessage, key=key, encrypted_image=encrypted_image)
print(received)
