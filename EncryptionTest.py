import rsa
import encrytionModule
import cv2


file_location = "encimg1.png"
message = 'Hello my name is Hamza'
print(message)
publicKey, privateKey = rsa.newkeys(512)
message = rsa.encrypt(message.encode('utf-8'), publicKey)
print(message)
print(str(message))
encoded_image, type = encrytionModule.encode_image(file_location, str(message))
cv2.imwrite("EncodedImage.png", encoded_image)
bingbong = encrytionModule.decode_image('EncodedImage.png')
output = rsa.decrypt(bingbong, privateKey).decode('utf-8')
print(output)
