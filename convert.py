def ToString(bytes): 
    return "".join(map(chr, bytes))

def ToHex(bytes):
    # return '[{}]'.format(' '.join(f"{x:02x}" for x in data))
    # return f'[{" ".join(f"{x:02x}" for x in data)}]'
    # return f'[{" ".join(map(lambda x: f"{x:02x}", data))}]'
    return f'[{" ".join(map("{:02x}".format, bytes))}]'
