import random
import numpy as np
from PIL import Image

message = "Hello World!"

# Encode the message in a serie of 8-bit values
b_message = ''.join(["{:08b}".format(ord(x)) for x in message ])
b_message = [int(x) for x in b_message]

b_message_lenght = len(b_message)

# Get the image pixel arrays 
def read_cover_image(filename):
    with Image.open(filename) as img:
        width, height = img.size
        data = np.array(img)    
    return data, width, height

def encrypt_steg_image(cover, message, seq = True, key = "STEGA"):
    input_length = len(message)
    if seq:
        # Add flag for seq with 7 at end, 25x
        for i in range(25):
            x = cover[i] // 10 * 10 + 7
            cover[i] = x - 10 if x > 255 else x
        
        # steg message
        for i in range(25,input_length+25):
            cover[i] = (cover[i] & ~1) | message[i-25]

        # Add flag for end message with 9 at end, 25x
        for j in range(25):
            i = input_length + 25 + j
            x = cover[i] // 10 * 10 + 9

            cover[i] = x - 10 if x > 255 else x

    else:
        # Add flag for random with 8 at begin, 25x
        for i in range(25):
            x = cover[i] // 10 * 10 + 8
            cover[i] = x - 10 if x > 255 else x

        # Add input length in next 10 bit, so max input length 9.999.999.999
        num_len = [int(x) for x in str(input_length)]
        z = 10 - len(num_len)
        for j in range(10):
            i = 25 + j
            if(j < z):
                x = cover[i] // 10 * 10 + 0
                cover[i] = x - 10 if x > 255 else x
            else:
                x = cover[i] // 10 * 10 + num_len[j - z]
                cover[i] = x - 10 if x > 255 else x

        # generate random post
        count = 0
        for i in key:
            count += ord(i)
        random.seed(count)
        pos = random.sample(range(35, len(cover)), input_length)
        idx = 0
        for i in pos:
            cover[i] = message[idx]
            idx += 1
    return cover

def decrypt_stegano_image(image, key = "STEGA"):
    identifier = []
    result = []
    # identify stegano using seq / random
    for i in range(25):
        identifier.append(image[i] % 10)

    if(identifier.count(7) == len(identifier)):
        # stegano using sequential
        count_flag = 0
        i = 25
        length_data = len(image) - 25
        while count_flag < 25 and i < length_data:
            result.append(image[i] % 2)
            if  image[i] % 10 == 9:
                count_flag += 1
            else:
                count_flag = 0
            i += 1
        # delete flag from message
        result = result[:-25]
    elif(identifier.count(8) == len(identifier)):
        # stegano using random
        input_length = int(''.join([str(x % 10) for x in image[25:35]]))

        count = 0
        for i in key:
            count += ord(i)
        random.seed(count)
        pos = random.sample(range(35, len(image)), input_length)
        idx = 0
        for i in pos:
            result.append(image[i] % 2)
    return result

# flatten image pixel
def flatten_image(data, width, height):
    return np.reshape(data, width*height*3)

# construct image pixel with size width*height
def construct_image(data, width, height):
    return np.reshape(data, (height, width, 3))

# test
data, width, height = read_cover_image('./test/sus.png')
data = flatten_image(data, width, height)
encrypt = encrypt_steg_image(data, b_message, False)
decrypt = decrypt_stegano_image(encrypt)

print(b_message)
print(decrypt)