import rsa
import encrytionModule
import cv2


file_location = "encimg1.jpeg"
message = 'Hello my name is Hamza'
print(message)
publicKey, privateKey = rsa.newkeys(512)
message = rsa.encrypt(message.encode(), publicKey)
print(publicKey)
print(message)
secret_message = str(message)
print(secret_message)
encoded_image = encrytionModule.encode_image(file_location, secret_message)
cv2.imwrite("EncodedImage.png", encoded_image)
bingbong = encrytionModule.decode_image('EncodedImage.png')
print(privateKey)
output = rsa.decrypt(bingbong, privateKey).decode()
# print(output)

