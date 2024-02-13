def ToString(bytes): 
    return "".join(map(chr, bytes))

def ToHex(bytes):
    # return '[{}]'.format(' '.join(f"{x:02x}" for x in data))
    # return f'[{" ".join(f"{x:02x}" for x in data)}]'
    # return f'[{" ".join(map(lambda x: f"{x:02x}", data))}]'
    return f'[{" ".join(map("{:02x}".format, bytes))}]'

def unsigned_16(b1, b2):
    return b1 | b2 << 8

def sign_extend(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)
