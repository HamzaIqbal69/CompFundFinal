import rsa
from sklearn.cross_decomposition import PLSCanonical
import cv2
import random
import pandas as pd

custom_key = pd.read_csv(r'/Users/hamza/CompFundFinal/decodekeynew.csv', sep=',', names=['character', 'byte'], header=None, skiprows=[0])
df = pd.DataFrame(data=custom_key)
df['character'] = df['character'].astype(str)
df['byte'] = df['byte'].astype(str)

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

def split(message):
  return [char for char in message]

def encode_custom(message):
  message_split = split(message)
  coded_message = ''
  for i in range(len(message_split)):
    j = message_split[i]
    try:
      coded_char = custom_key.loc[custom_key['character'] == j, 'byte'].iloc[0]
    except:
      print('unrecognized character')
      coded_char = '@@@'
    
    coded_message += coded_char
  return coded_message, 'custom'

def decode_custom(message):
  output = []
  for i in range(0, len(message), 2):
    j = message[i:i+2]
    index_nb = df[df.eq(j).any(1)]
    df2 = index_nb['character'].tolist()
    s = [str(x) for x in df2]
    output += s
  output = ''.join(output)
  return output

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
          cv2.imwrite("EncodedImage.png", img)
          return 'EncodedImage.png', 'img'

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
          return message

def encode_rsa(message):
  publicKey, privateKey = rsa.newkeys(512)
  secret_message = rsa.encrypt(message.encode(), publicKey)
  return secret_message, 'rsa', privateKey

def decode_rsa(message, privatekey):
  output = rsa.decrypt(message, privatekey).decode()
  return output

def encode_random(message):
  enc_type_lst = ['rsa', 'img', 'custom']
  enc_type = random.choice(enc_type_lst)
  if enc_type == 'rsa':
    secret_message, enc_type, key = encode_rsa(message)
    return enc_type, secret_message, key, None
  if enc_type == 'img':
    file_location = 'encimg1.png'
    encrypted_image, enc_type = encode_image(image_location=file_location, msg=message)
    return enc_type, None, None, encrypted_image
  if enc_type == 'custom':
    secret_message, enc_type = encode_custom(message)
    return enc_type, secret_message, None, None

def decode_random(enc_type, secret_message, key, encrypted_image):
  if enc_type == 'rsa':
    message = decode_rsa(secret_message, key)
    return message
  if enc_type == 'img':
    message = decode_image(encrypted_image)
    return message
  if enc_type == 'custom':
    message = decode_custom(secret_message)
    return message
