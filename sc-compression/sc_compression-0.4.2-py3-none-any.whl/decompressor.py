import lzma
import lzham
import zstandard

from sc_compression.signatures import Signatures
from sc_compression.utils.reader import Reader


class Decompressor(Reader):
    def __init__(self):
        super().__init__(b'')
        self.signatures = Signatures()

    def decompress(self, buffer: bytes) -> bytes:
        super().__init__(buffer, 'little')

        signature = self.signatures.get_signature(self.buffer)
        if signature is Signatures.NONE:
            return buffer
        elif signature == Signatures.SC:
            buffer = buffer[26:]
            decompressed = self.decompress(buffer)
        elif signature == Signatures.SIG:
            buffer = buffer[68:]
            decompressed = self.decompress(buffer)
        elif signature == Signatures.SCLZ:
            self.read(30)
            dict_size_log2 = self.readUByte()
            uncompressed_size = self.readInt32()

            filters = {
                'dict_size_log2': dict_size_log2
            }
            decompressed = lzham.decompress(self.buffer[35:], uncompressed_size, filters)
        elif signature == Signatures.LZMA:
            decompressor = lzma.LZMADecompressor()
            compressed = self.buffer[:5] + b'\xff' * 8 + self.buffer[9:]

            decompressed = decompressor.decompress(compressed)
        elif signature == Signatures.ZSTD:
            decompressor = zstandard.ZstdDecompressor()
            decompressed = decompressor.decompress(self.buffer)
        else:
            raise TypeError(signature)

        return decompressed
