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

def encrypt_steg_image(cover, message, seq):
    input_length = len(message)
    if seq:
        # change first 10th lsb bit to 11 if sequential, else 11
        for i in range(10):
            cover[i] = cover[i] | (1 << (2 - 1))
            cover[i] = cover[i] | (1 << (1 - 1))
        
        # steg message
        for i in range(10,input_length+10):
            cover[i] = (cover[i] & ~1) | message[i-10]

        # Add flag for end message with 9 at end, 25x
        for j in range(25):
            i = input_length + 10 + j
            x = cover[i] // 10 * 10 + 9

            cover[i] = x - 10 if x > 255 else x

    else:
        # change first 10th lsb bit to 11 if sequential, else 00
        for i in range(10):
            cover[i] = cover[i] & ~(1 << (2 - 1))
            cover[i] = cover[i] & ~(1 << (1 - 1))

        # do random encrypt thing


    return cover

def decrypt_stegano_image(image, key):
    identifier = []
    result = []
    # identify stegano using seq / random
    for i in range(10):
        identifier.append(image[i] % 3)

    if(identifier.count(0) == len(identifier)):
        # stegano using sequential
        count_flag = 0
        i = 10
        length_data = len(image) - 10
        while count_flag < 25 and i < length_data:
            result.append(image[i] % 2)
            if  image[i] % 10 == 9:
                count_flag += 1
            else:
                count_flag = 0
            i += 1
        # delete flag from message
        result = result[:-25]
    elif(identifier.count(1) == len(identifier)):
        # stegano using random
        print("DOR")

    return result

# flatten image pixel
def flatten_image(data, width, height):
    return np.reshape(data, width*height*3)

# construct image pixel with size width*height
def construct_image(data, width, height):
    return np.reshape(data, (height, width, 3))

data, width, height = read_cover_image('./test/sus.png')
data = flatten_image(data, width, height)
encrypt = encrypt_steg_image(data, b_message, True)
decrypt = decrypt_stegano_image(encrypt, 'key')

print(b_message)
print(decrypt)
# # Reshape back to an image pixel array
# data = np.reshape(data, (height, width, 3))

# new_img = Image.fromarray(data)
# new_img.save("cover-secret.png")
# new_img.show()