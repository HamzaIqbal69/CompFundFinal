import rsa
from sklearn.cross_decomposition import PLSCanonical
import cv2


def char_generator(message):
  for c in message:
    yield ord(c)

def get_image(image_location):
  img = cv2.imread(image_location)
  return img

def gcd(x, y):
  while(y):
    x, y = y, x % y

  return x

def encode_image(image_location, msg):
  img = get_image(image_location)
  msg_gen = char_generator(msg)
  pattern = gcd(len(img), len(img[0]))
  for i in range(len(img)):
    for j in range(len(img[0])):
      if (i+1 * j+1) % pattern == 0:
        try:
          img[i-1][j-1][0] = next(msg_gen)
        except StopIteration:
          img[i-1][j-1][0] = 0
          return img, 'img'

def decode_image(img_loc):
  img = get_image(img_loc)
  pattern = gcd(len(img), len(img[0]))
  message = ''
  for i in range(len(img)):
    for j in range(len(img[0])):
      if (i-1 * j-1) % pattern == 0:
        if img[i-1][j-1][0] != 0:
          message = message + chr(img[i-1][j-1][0])
        else:
          return message.encode('utf-8')

def encode_rsa(message):
  publicKey, privateKey = rsa.newkeys(512)
  secret_message = rsa.encrypt(message.encode('utf-8'), publicKey)
  return secret_message, 'rsa', privateKey


def decode_rsa(message, privatekey):
  output = rsa.decrypt(message, privatekey).decode('utf-8')
  return output
