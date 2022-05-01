######################################################################################
# This is the module that provides the security functions to both the client and     #
# server programs.                                                                   #
# There are currently 3 implemented forms of encryption in the client and server     # 
# classes.  The three types of encryption are as follows:                            #
#             - RSA encryption, this is provided by python and I am implementing the #
#               built in functions in my rsa encryption function                     #
#             - Vigneres Cipher, this is a famous method of encrypting text and I    #
#               implemented it in python as a form of encryption                     #
#             - Custom Cipher, uses a csv file that contains a random encoding of    #
#               characters to different characters as the key, and then just shifts  #
#               the messages using that key                                          #
######################################################################################

# Imports ----------------------------------------------------------------------------

import rsa
import cv2
import random
import pandas as pd

# Module Variable Creation -----------------------------------------------------------

custom_key = pd.read_csv(r'/Users/hamza/CompFundFinal/decodekeynew.csv', sep=',', names=['character', 'byte'], header=None, skiprows=[0])
df = pd.DataFrame(data=custom_key)
df['character'] = df['character'].astype(str)
df['byte'] = df['byte'].astype(str)
chars_set = '`1234567890-=qwertyuiop[]asdfghjkl;''":zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP}{|ASDFGHJKLZXCVBNM<> '
key_lst = ['armenian', 'cucumber', 'michigan', 'shelby', 'motherly']
char_to_index = dict(zip(chars_set, range(len(chars_set))))
index_to_char = dict(zip(range(len(chars_set)), chars_set))

# Functions --------------------------------------------------------------------------

def char_generator(message):
  """
  Turns the message into a list of characters, helper function for encode_image 
  and decode_image functions
  """
  for c in message:
    yield ord(c)

def get_image(image_location):
  """
  Reads an image to a csv file, helper function to encode_image and decode_image 
  functions
  """
  img = cv2.imread(image_location)
  return img

def gcd(x, y):
  """
  Finds greatest common denominator of two numbers, helper function for encode_image 
  and decode_image functions
  """
  while(y):
    x, y = y, x % y

  return x

def split(message):
  """
  Splits message into list of charcters, helper function for encode_custom function
  """
  return [char for char in message]

def encode_custom(message):
  """
  Uses a key that is derived from a csv file, and maps the characters in the message
  to the characters from the key
  """
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
  return coded_message

def decode_custom(message):
  """
  Uses the same key as encode_custom to map the encoded characters back to the original
  characters of the message
  """
  output = []
  for i in range(0, len(message), 2):
    j = message[i:i+2]
    index_nb = df[df.eq(j).any(1)]
    df2 = index_nb['character'].tolist()
    s = [str(x) for x in df2]
    output += s
  output = ''.join(output)
  return output

def encode_Vig(message):
  """
  Uses vigneres cipher to encode the message using a random key, that is generated from
  the key list that was declared as a module variable, then uses Vigneres cipering method
  to scramble the letters of the message
  """
  key = random.choice(key_lst)
  encoded = ''
  split_message = [message[i:i + len(key)] for i in range(0, len(message), len(key))]
  for split in split_message:
    i = 0
    for letter in split:
      num = (char_to_index[letter] + char_to_index[key[i]]) % len(chars_set)
      encoded += index_to_char[num]
      i += 1
  return encoded, key

def decode_Vig(message, key):
  """
  Uses vigneres method and the key generated from teh encode_Vig function to decrypt 
  the message
  """
  decoded = ''
  split_message = [message[i:i + len(key)] for i in range(0, len(message), len(key))]
  for split in split_message:
    i = 0
    for letter in split:
      num = (char_to_index[letter] - char_to_index[key[i]]) % len(chars_set)
      decoded += index_to_char[num]
      i += 1
  return decoded

def encode_image(image_location, msg):
  """
  Uses an image file as the method for encryption, by converting it to a 
  bit array and changing the first bit of each pixel value to the associated
  character in the array, returns the encoded image
  """
  img = get_image(image_location)
  msg_gen = char_generator(msg)
  pattern = gcd(len(img), len(img[0]))
  if img:
    for i in range(len(img)):
      for j in range(len(img[0])):
        if (i+1 * j+1) % pattern == 0:
          try:
            img[i-1][j-1][0] = next(msg_gen)
          except StopIteration:
            img[i-1][j-1][0] = 0
            cv2.imwrite("EncodedImage.png", img)
            return 'EncodedImage.png', 'img', img

def decode_image(img_loc):
  """
  Takes the encoded image looks at the first bit in every pixel
  and creates a message using the character values of each of those
  bits
  """
  img = get_image(img_loc)
  pattern = gcd(len(img), len(img[0]))
  message = ''
  if img:
    for i in range(len(img)):
      for j in range(len(img[0])):
        if (i-1 * j-1) % pattern == 0:
          if img[i-1][j-1][0] != 0:
            message = message + chr(img[i-1][j-1][0])
          else:
            return message

def encode_rsa(message):
  """
  Implements pythons built in encryption methods
  """
  publicKey, privateKey = rsa.newkeys(512)
  secret_message = rsa.encrypt(message.encode(), publicKey)
  return secret_message, privateKey

def decode_rsa(message, privatekey):
  """
  Implements pythons built in encryption methods
  """
  output = rsa.decrypt(message, privatekey).decode()
  return output

def encode_random(message):
  """
  Chooses a random type of encryption from the list of avaiable encryption
  method types, and depending on the selection implements the corresponding
  encryption method, this makes the module easy to encrypt in both the client
  and server because you only have to add one line and you can still use all
  the different types of encryption
  """
  enc_type_lst = ['rsa', 'custom', 'Vig']
  enc_type = random.choice(enc_type_lst)
  if enc_type == 'rsa':
    secret_message, key = encode_rsa(message)
    return enc_type, secret_message, key
  if enc_type == 'custom':
    secret_message = encode_custom(message)
    return enc_type, secret_message, None
  if enc_type == 'Vig':
    secret_message, key = encode_Vig(message)
    return enc_type, secret_message, key

def decode_random(enc_type, secret_message, key):
  """
  Using the type of encryption, decodes the message accordingly
  """
  if enc_type == 'rsa':
    message = decode_rsa(secret_message, key)
    return message
  if enc_type == 'custom':
    message = decode_custom(secret_message)
    return message
  if enc_type == 'Vig':
    message = decode_Vig(secret_message, key)
    return message