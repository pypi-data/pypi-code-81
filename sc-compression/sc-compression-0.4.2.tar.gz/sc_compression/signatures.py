import re


class Signatures:
    LZMA = 2 ** 0
    SC = 2 ** 1
    SCLZ = 2 ** 2
    SIG = 2 ** 3
    ZSTD = 2 ** 4
    NONE = 2 ** 5

    def __init__(self):
        self.last_signature: int = -1

    def get_signature(self, buffer) -> int:
        signature = Signatures.NONE
        if re.match(b'\x00\x00?\x00', buffer[1:5]):  # SC Dict size
            signature = Signatures.LZMA
        elif self.last_signature == Signatures.SC:
            signature = Signatures.ZSTD
            self.last_signature = -1

        if buffer.startswith(b'SC'):
            if len(buffer) >= 30 and buffer[26:30] == b'SCLZ':
                signature = Signatures.SCLZ
            else:
                signature = Signatures.SC
        elif buffer[:4] == b'Sig:':
            signature = Signatures.SIG

        self.last_signature = signature

        return signature
