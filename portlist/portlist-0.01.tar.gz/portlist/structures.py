from ctypes import Structure
from ctypes.wintypes import DWORD, WORD, BYTE, PULONG
import ctypes


# Structures
class GUID(Structure):
    _fields_ = [
        ('Data1', DWORD),
        ('Data2', WORD),
        ('Data3', WORD),
        ('Data4', BYTE * 8)
    ]

    def __str__(self):
        return "{{{:08x}-{:04x}-{:04x}-{}-{}}}".format(
            self.Data1,
            self.Data2,
            self.Data3,
            ''.join(["{:02x}".format(d) for d in self.Data4[:2]]),
            ''.join(["{:02x}".format(d) for d in self.Data4[2:]]),
        )

    def __getitem__(self, item):
        return getattr(self, item)


class SP_DEVINFO_DATA(ctypes.Structure):  # noqa
    _fields_ = [
        ('cbSize', DWORD),
        ('ClassGuid', GUID),
        ('DevInst', DWORD),
        ('Reserved', PULONG)
    ]
