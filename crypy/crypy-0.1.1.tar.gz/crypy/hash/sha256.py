import copy
import struct
import binascii

__base__ = 'https://gist.github.com/prokls/41e82472bd4968720d1482f81235e0ac'
__license__ = 'MIT'


class SHA256:
    _k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
          0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
          0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
          0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
          0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
          0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
          0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
          0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
          0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
          0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
          0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
          0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
          0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
          0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
          0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
          0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

    _h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
          0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

    @staticmethod
    def _pad(msg_len):
        mdi = msg_len & 0x3F
        length = struct.pack('!Q', msg_len << 3)

        if mdi < 56:
            padlen = 55 - mdi
        else:
            padlen = 119 - mdi

        return b'\x80' + (b'\x00' * padlen) + length

    @staticmethod
    def _ror(x, y):
        return ((x >> y) | (x << (32 - y))) & 0xFFFFFFFF

    @staticmethod
    def _maj(x, y, z):
        return (x & y) ^ (x & z) ^ (y & z)

    @staticmethod
    def _ch(x, y, z):
        return (x & y) ^ ((~x) & z)

    _output_size = 8
    block_size = 64
    digest_size = 32

    def __init__(self, m=None, state=None, counter=None):
        self._counter = 0
        self._cache = b''
        self._k = copy.deepcopy(self._k)
        self._h = copy.deepcopy(self._h)

        if state is not None and counter is not None:
            self._h = state
            self._counter = counter
        if m is not None:
            self.update(m)

    @classmethod
    def clone(cls, secret_len, base, base_hash):
        base_padded = base+cls._pad(secret_len + len(base))

        state = [int.from_bytes(base_hash[i:i+4], byteorder="big") for i in range(0, len(base_hash), 4)]
        h = SHA256(state=state, counter=secret_len + len(base_padded))
        return base_padded, h

    def _compress(self, c):
        w = [0] * 64
        w[0:16] = struct.unpack('!16L', c)

        for i in range(16, 64):
            s0 = self._ror(w[i - 15], 7) ^ self._ror(w[i - 15], 18) ^ (w[i - 15] >> 3)
            s1 = self._ror(w[i - 2], 17) ^ self._ror(w[i - 2], 19) ^ (w[i - 2] >> 10)
            w[i] = (w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFF

        a, b, c, d, e, f, g, h = self._h

        for i in range(64):
            s0 = self._ror(a, 2) ^ self._ror(a, 13) ^ self._ror(a, 22)
            t2 = s0 + self._maj(a, b, c)
            s1 = self._ror(e, 6) ^ self._ror(e, 11) ^ self._ror(e, 25)
            t1 = h + s1 + self._ch(e, f, g) + self._k[i] + w[i]

            h = g
            g = f
            f = e
            e = (d + t1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xFFFFFFFF

        for i, (x, y) in enumerate(zip(self._h, [a, b, c, d, e, f, g, h])):
            self._h[i] = (x + y) & 0xFFFFFFFF

    def update(self, m):
        if not m:
            return

        if type(m) == str:
            m = m.encode()

        self._counter += len(m)
        m = self._cache + m

        for i in range(0, len(m) // 64):
            self._compress(m[64 * i:64 * (i + 1)])
        self._cache = m[-(len(m) % 64):]

        return self

    def digest(self):
        r = copy.deepcopy(self)
        r.update(self._pad(self._counter))
        data = [struct.pack('!L', i) for i in r._h[:self._output_size]]
        return b''.join(data)

    def hexdigest(self):
        return binascii.hexlify(self.digest()).decode('ascii')
