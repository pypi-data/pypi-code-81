import io
import math
import struct

from collections import defaultdict

from tap_file import HeaderType, TapFileReader, TapHeader

from cbm_shell.tap_image_path import TapImagePath


class FileData(io.BytesIO):
    def open(self):
        self.seek(0)
        return self

    def close(self):
        pass


class TapImage:
    def __init__(self, path, mode, drive):
        self.drive = drive
        self.filepath = path
        self.writeable = False
        self.cache = None

    def close(self):
        pass

    def _load_cache(self):
        if self.cache is None:
            self.cache = []

            name_count = defaultdict(int)
            tap = TapFileReader(self.filepath)
            for obj in tap.contents():
                if isinstance(obj, TapHeader):
                    if obj.htype in (HeaderType.PRG_RELOC, HeaderType.PRG, HeaderType.SEQ):
                        suffix = "~{}".format(name_count[obj.name] if name_count[obj.name] else '')
                        if suffix == '~' and obj.name:
                            suffix = ''
                        obj.unique_name = obj.name+suffix.encode()
                        current_data = FileData()
                        if obj.htype in (HeaderType.PRG_RELOC, HeaderType.PRG):
                            # prepend the program start address for equivalence with disk files
                            current_data.write(struct.pack('<H', obj.start))
                        self.cache.append((obj, current_data))
                        name_count[obj.name] += 1
                else:
                    # PRG or SEQ data
                    current_data.write(obj.data)

    def path(self, name):
        self._load_cache()
        for header, data in self.cache:
            if name == header.unique_name:
                return TapImagePath(self.drive, header, data)
        raise FileNotFoundError("File not found: "+str(name))

    def glob(self, name):
        return []

    def expand(self, name):
        self._load_cache()
        for header, data in self.cache:
            if header.unique_name.startswith(name):
                yield TapImagePath(self.drive, header, data)

    def directory(self, pattern=b'', encoding='petscii-c64en-uc', drive=0):
        yield "{} <TAP image>".format(drive)
        self._load_cache()

        for header, _ in self.cache:
            if header.name.startswith(pattern):
                size_blocks = math.ceil((header.end-header.start)/254)
                name = '"'+header.name.decode(encoding)+'"'
                yield "{:5}{:18} {!s}".format(str(size_blocks), name, header.htype)

    def __str__(self):
        return "TapImage({!s})".format(self.filepath)
