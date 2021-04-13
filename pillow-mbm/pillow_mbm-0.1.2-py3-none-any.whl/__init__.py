from pillow_mbm.version import __version__

import struct
from PIL import Image, ImageFile

MAGIC = b'\x03KSP'


def _accept(prefix: bytes):
    """Check if a file is a MBM file"""
    return prefix[:4] == MAGIC


class MBMImageFile(ImageFile.ImageFile):
    format = 'MBM'
    format_description = 'Kerbal Space Program MBM image'

    def _open(self):
        """Open an MBM file"""
        magic = self.fp.read(4)
        if magic != MAGIC:
            raise SyntaxError('not a MBM file')

        width, height, bits = struct.unpack('<2I4xI', self.fp.read(16))

        self._size = (width, height)

        if bits == 24:
            self.mode = 'RGB'
        elif bits == 32:
            self.mode = 'RGBA'
        else:
            raise SyntaxError('unknown number of bits')

        self.tile = [('raw', (0, 0, width, height), 20, (self.mode, 0, 1))]


Image.register_open(MBMImageFile.format, MBMImageFile, _accept)
Image.register_extensions(MBMImageFile.format, ['.mbm'])
