import wave
import random

def read_audio(filename:str):
    with wave.open(filename) as fd:
        params = fd.getparams()
        frames = fd.readframes(-1)
    return params, frames

def create_audio(filename, params, frames):
    # Create audio file for insertion message
    with wave.open(filename, 'wb') as fd:
        # fd.setparams(params)
        fd.writeframes(frames)


def encrypt_audio(message, filename, seq=True, key="STEGA"):
    # bytes to binary message
    binary_message = []
    for i in range(len(message)):
        binary_message.append(bin(message[i]))

    for i in range(len(binary_message)):
        binary_message[i] = binary_message[i][2:]
        
    for i in range(len(binary_message)):
        while len(binary_message[i]) != 8:
            binary_message[i] = "0"+binary_message[i]

    b_message = ""
    for i in range(len(binary_message)):
        b_message += binary_message[i]

    # read audio
    params, audio = read_audio(filename)

    #convert bytes to bytearray
    audio = bytearray(audio)

    # Adding flag to distinguish between seq and random
    
    if seq: # if sequence
        for i in range(25):
            if audio[i] % 2 == 1:
                audio[i] -= 1
        # Inserting message
        for j in range (len(b_message)):
            if audio[i+j+1] % 2 == 0:
                audio[i+j+1] += int(b_message[j])
            else:
                if int(b_message[j]) == 0:
                    audio[i+j+1] -= 1

            # Adding flag 1111111...[25] in binary as end of message sign          
        for k in range(25):
            if int(audio[i+j+k+1+1]) % 2 == 0:
                audio[i+j+k+1+1] += 1         

    else: # if random
        for i in range(25):
            if audio[i] % 2 == 0:
                audio[i] += 1
        
        length_message = str(len(b_message))
        while (len(length_message)) != 10:
            length_message = "0"+length_message

        for i in range(25,35):
            audio[i] = int(length_message[i-25])
        count = 0
        # generate pseudo-random posision
        for i in key:
            count += ord(i)
        random.seed(count)
        pos = random.sample(range(35, len(audio)), len(b_message))
        idx = 0
        for i in pos:
            if audio[i] % 2 == 0:
                audio[i] += int(b_message[idx])
            else:
                if int(binary_message[idx]) == 0:
                    audio[i] -= 1
            idx += 1

    #stegano audio
    return params, audio
    # create_audio('output.wav', params, audio)


def decrypt_audio(filename, key="STEGA"):
    # Read stegano audio
    params, audio = read_audio(filename)

    binary_audio = []
    flag_count = 0

    c_seq = 0
    c_rand = 0

    for i in range(25):
        if int(audio[i]) % 2 == 0:
            c_seq += 1
        else:
            c_rand += 1

    i += 1

    if c_seq == 25:
        # Check end of message using flag_count
        while flag_count < 25 and i < len(audio):
            if int(audio[i]) % 2 == 1:
                flag_count += 1
            else:
                flag_count = 0
            binary_audio.append(bin(audio[i]))
            i += 1
        
        #get message
        result = ""
        for i in range(len(binary_audio)):
            if int(binary_audio[i][2:]) % 2 == 0:
                result += "0"
            else:
                result += "1"
        
        result = result[:-25]
    elif c_rand == 25:

        # get length_message
        length_message = ""
        for i in range(25,35):
            length_message = length_message + str(audio[i])
        length_message = int(length_message)

        
        # generate pseudo-random posision
        count = 0
        for i in key:
            count += ord(i)
        random.seed(count)
        pos = random.sample(range(35, len(audio)), length_message)
        
        # get message
        result = ""

        for i in pos:
            if int(bin(audio[i])[2:]) % 2 == 0:
                result += "0"
            else:
                result += "1"
    
    # string to bin
    a = []
    for i in range(0, len(result), 8):
        a.append(int(result[i:i+8], 2).to_bytes(1, 'big'))

    result = b""
    for i in range(len(a)):
        result += a[i]

    return result


# message = b'\x00\x00\x66\x20'
# encrypt_audio(message, 'test/opera.wav')
# print(decrypt_audio('output.wav'))

# with wave.open('output.wav') as fd:
#     params = fd.getparams()
#     frames = fd.readframes(-1)

