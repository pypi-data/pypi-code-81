import math
import copy
import binascii


class MD5:
    rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                      5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
                      4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                      6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

    constants = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xFFFFFFFF for i in range(64)]

    _state = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

    functions = 16 * [lambda b, c, d: (b & c) | (~b & d)] + \
                16 * [lambda b, c, d: (d & b) | (~d & c)] + \
                16 * [lambda b, c, d: b ^ c ^ d] + \
                16 * [lambda b, c, d: c ^ (b | ~d)]

    index_functions = 16 * [lambda i: i] + \
                      16 * [lambda i: (5 * i + 1) % 16] + \
                      16 * [lambda i: (3 * i + 5) % 16] + \
                      16 * [lambda i: (7 * i) % 16]

    def __init__(self, m=None, state=None, counter=None):
        self._cache = b''
        self._counter = 0
        self._state = copy.deepcopy(self._state)

        if state is not None and counter is not None:
            self._state = state
            self._counter = counter
        if m is not None:
            self.update(m)

    def update(self, m):
        if type(m) == str:
            m = m.encode()

        self._counter += len(m)
        m = self._cache + m

        for i in range(0, len(m) // 64):
            self._compress(m[64 * i:64 * (i + 1)])
        self._cache = m[-(len(m) % 64):]

        return self

    @staticmethod
    def rol(x, amount):
        x &= 0xFFFFFFFF
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

    @staticmethod
    def _pad(msg_len):
        pad = b"\x80"
        while (msg_len + len(pad)) % 64 != 56:
            pad += b"\x00"
        pad += ((8 * msg_len) & 0xffffffffffffffff).to_bytes(8, byteorder='little')
        return pad

    def _compress(self, message):
        for chunk_ofst in range(0, len(message), 64):
            a, b, c, d = self._state
            chunk = message[chunk_ofst:chunk_ofst + 64]
            for i in range(64):
                f = self.functions[i](b, c, d)
                g = self.index_functions[i](i)
                to_rotate = a + f + self.constants[i] + int.from_bytes(chunk[4 * g:4 * g + 4], byteorder='little')
                new_b = (b + self.rol(to_rotate, self.rotate_amounts[i])) & 0xFFFFFFFF
                a, b, c, d = d, new_b, b, c
            for i, val in enumerate([a, b, c, d]):
                self._state[i] += val
                self._state[i] &= 0xFFFFFFFF

    def digest(self):
        r = copy.deepcopy(self)
        r.update(self._pad(r._counter))
        return (sum(x << (32 * i) for i, x in enumerate(r._state))).to_bytes(16, byteorder='little')

    @classmethod
    def clone(cls, secret_len, base, base_hash):
        base_padded = base + cls._pad(secret_len + len(base))

        state = [int.from_bytes(base_hash[i:i + 4][::-1], byteorder="big") for i in range(0, len(base_hash), 4)]
        h = MD5(state=state, counter=secret_len + len(base_padded))
        return base_padded, h

    def test(self):
        r = copy.deepcopy(self)
        r.update(self._pad(r._counter))

    def hexdigest(self):
        return binascii.hexlify(self.digest()).decode('ascii')
