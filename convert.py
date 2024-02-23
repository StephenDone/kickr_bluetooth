def ToString(bytes): 
    return "".join(map(chr, bytes))

def ToHex(bytes):
    # return '[{}]'.format(' '.join(f"{x:02x}" for x in data))
    # return f'[{" ".join(f"{x:02x}" for x in data)}]'
    # return f'[{" ".join(map(lambda x: f"{x:02x}", data))}]'
    return f'[{" ".join(map("{:02x}".format, bytes))}]'

def unsigned_16(b1, b2):
    return b1 | b2 << 8

def signed_16(b1, b2):
    return sign_extend(unsigned_16(b1, b2), 16)

def sign_extend(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

def unsigned_32(b1, b2, b3, b4):
    return b1 \
        | (b2 << 8) \
        | (b3 << 16) \
        | (b4 << 24) 
    