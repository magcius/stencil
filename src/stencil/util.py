
def nbits(num):
    """
    The number of bits in the absolute value of `num`.
    """
    return len(bin(abs(num))) - 2

def nbytes(num):
    """
    The number of bytes in `num`, assuming two's complement notation.
    """
    if num < 0:
        num = ~num + 1

    if num & 7:
        return num >> 3 + 1
    return num >> 3

def decode_bytes(bytes):
    """
    Decode `bytes` into an integer.
    """
    num = 0
    for char in bytes:
        num <<= 8
        num |= ord(char)
    return num

def encode_int(num, length):
    bytes = []
    for i in xrange(length):
        bytes.append(chr(num & 0xFF))
        num >>= 8
    return ''.join(bytes)
