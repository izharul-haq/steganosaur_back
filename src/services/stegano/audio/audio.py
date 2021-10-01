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
        fd.setparams(params)
        fd.writeframes(frames)


def encrypt_audio(binary_message, filename, seq=True, key="STEGA"):
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
        for j in range (len(binary_message)):
            if audio[i+j+1] % 2 == 0:
                audio[i+j+1] += int(binary_message[j])
            else:
                if int(binary_message[j]) == 0:
                    audio[i+j+1] -= 1

            # Adding flag 1111111...[25] in binary as end of message sign          
        for k in range(25):
            if int(audio[i+j+k+1+1]) % 2 == 0:
                audio[i+j+k+1+1] += 1         

    else: # if random
        for i in range(25):
            if audio[i] % 2 == 0:
                audio[i] += 1
        
        length_message = str(len(binary_message))
        while (len(length_message)) != 10:
            length_message = "0"+length_message

        for i in range(25,35):
            # print(audio[i])
            audio[i] = int(length_message[i-25])
            # print(audio[i])
        count = 0
        # generate pseudo-random posision
        for i in key:
            count += ord(i)
        random.seed(count)
        pos = random.sample(range(35, len(audio)), len(binary_message))
        idx = 0
        for i in pos:
            if audio[i] % 2 == 0:
                audio[i] += int(binary_message[idx])
            else:
                if int(binary_message[idx]) == 0:
                    audio[i] -= 1
            idx += 1

    #stegano audio
    create_audio('output.wav', params, audio)

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
        
        return result[:-25]
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
        return result
