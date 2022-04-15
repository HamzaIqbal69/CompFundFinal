from numpy import rec
import rsa
import security
import cv2


# file_location = "encimg1.png"
# message = 'Hello my name is Hamza'
# print(message)
# secretmessage, enc_type, key = security.encode_rsa(message)
# print(secretmessage)
# receivedmessage = security.decode_rsa(secretmessage, key)
# print(receivedmessage)

# encrypted_image, enc_type = security.encode_image(image_location=file_location, msg=message)
# receivedmessage = security.decode_image(encrypted_image)
# print(receivedmessage)
message = 'Hello im all encrpted so cool'
enc_type, secretmessage, key, encrypted_image = security.encode_random(message)
print(f'Encoding Type: {enc_type}\nMessage: {secretmessage}\nKey: {key}\nImage: {encrypted_image}')
received = security.decode_random(enc_type=enc_type, secret_message=secretmessage, key=key, encrypted_image=encrypted_image)
print(received)





