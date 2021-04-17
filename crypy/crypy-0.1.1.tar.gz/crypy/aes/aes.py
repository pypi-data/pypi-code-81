import math
from Crypto.Util.strxor import strxor


def postfix_attack(oracle, prefix_len=0):
    found = b"A"*15
    n_blocks = len(oracle(b""))//16

    offset = math.ceil(prefix_len/16)

    for b in range(n_blocks-offset):
        for i in range(16):
            for j in range(256):
                new_byte = bytes([j])
                block0 = b"P"*(16 - (prefix_len % 16)) if prefix_len % 16 != 0 else b""
                block1 = found[-15:] + new_byte
                block2 = b"A"*(15-i)
                ct = oracle(block0+block1+block2)
                ct_blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
                if ct_blocks[offset+0] == ct_blocks[offset+b+1]:
                    found += new_byte
                    break

    if prefix_len % 16 == 0:
        return found[15:-1]
    else:
        return found[15:]


def padding_oracle_attack(oracle, ct):
    blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]

    founds = []
    for i in range(1, len(blocks))[::-1]:
        found = b""
        for j in range(1, 17):
            base_xor = b"\x00"*(16*(i-1)) + b"\x00"*(16-j) + bytes([j])*j + b"\x00"*16
            for k in range(0, 256):
                if k == j:
                    continue
                new_byte = bytes([k])
                xor = b"\x00"*(16*(i-1)) + b"\x00"*(16-j) + new_byte + found + b"\x00"*16

                if oracle(strxor(base_xor, strxor(b"".join(blocks[:i+1]), xor))):
                    found = new_byte + found
                    break
            else:
                found = bytes([j]) + found
        founds = [found] + founds
    return b"".join(founds)
