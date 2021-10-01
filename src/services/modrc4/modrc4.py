from .utils import init_stream

S1 = [i for i in range(256)]
S2 = [i for i in range(255, -1, -1)]


def crypt(_input, key: bytes) -> bytes:
    '''Encrypt or decrypt given input with given key
    using modified RC4 alogrithm.'''

    stream = init_stream(S1, key)
    inv_stream = init_stream(S2, key)

    i = 0
    j1 = 0
    j2 = 0

    res = []
    for idx in range(0, len(_input)):
        i = (i+1) % 256

        j1 = (j1 + stream[i]) % 256
        stream[i], stream[j1] = stream[j1], stream[i]

        j2 = (j2 + inv_stream[i]) % 256
        inv_stream[i], inv_stream[j2] = inv_stream[j2], inv_stream[i]

        keystream_idx = (stream[j1] + inv_stream[j2]) % 256
        keystream = stream[keystream_idx]

        res.append((keystream ^ _input[idx]).to_bytes(1, byteorder='big'))

    return b''.join(res)
