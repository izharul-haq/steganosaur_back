def init_stream(s: list[int], key: bytes) -> list[int]:
    '''Initialize permutation in stream'''

    res = s.copy()
    key_length = len(key)

    j = 0
    for i in range(256):
        j = (j + res[i] + key[i % key_length]) % 256
        res[i], res[j] = res[j], res[i]

    return res
